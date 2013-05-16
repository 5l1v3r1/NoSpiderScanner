from tornado.escape import native_str, parse_qs_bytes, utf8
from tornado import httputil
import tornado.httpserver
from tornado.log import gen_log
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import hashlib
import ast

from myconfigparser import get_list
from tornado.httpserver import _BadRequestException
from tornado.options import define, options
define("port", default=8080)


def parse_request(data):
    try:
        req = ast.literal_eval(data)
        path, sep, query = req['uri'].partition('?')
        get_arguments = parse_qs_bytes(query, keep_blank_values=True)
        post_arguments = parse_qs_bytes(req['body'], keep_blank_values=True)
        host = req['headers']['Host']
        headers = req['headers']
        return headers, host, path, get_arguments, post_arguments
    except _BadRequestException as e:
        gen_log.info("Malformed HTTP request:%s", e)
        return


def gen_uniqcode(path, get_arg, post_arg):
        MVC_PARAMS = get_list('config.ini', 'MVC Params', 'paramList')
        args = {}
        args.update(get_arg)
        args.update(post_arg)
        keys = ''
        for key in sorted(args.iterkeys()):
            if key in MVC_PARAMS:
                key += '=' + args[key][0]
            keys += key
            keys += '&'
        uniq_qry = path + '?' + keys
        m = hashlib.md5()
        m.update(uniq_qry)
        uniq_code = m.hexdigest()
        return uniq_code


class Applicaion(tornado.web.Application):

    def __init__(self):
        handlers = [(r"/collect", CollectHandler),
                    (r"/", IndexHandler)]
        self.conn = pymongo.Connection("localhost", 27017)
        self.db = self.conn["reqs"]
        tornado.web.Application.__init__(self, handlers, debug=True)


class CollectHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def post(self):
        user_name = self.get_argument("username", "anonymous")
        internal_ip = self.get_argument("ip", "None")
        req = self.request.arguments.get("request", [""])[0]
        headers, host, path, get_arg, post_arg = parse_request(req)
        uniq_code = gen_uniqcode(path, get_arg, post_arg)
        self.db.requests.insert(
            {"_id": uniq_code, "host": host, "headers": headers,
                               "path": path, "get_arg": get_arg,
                               "post_arg": post_arg})
        self.write(uniq_code)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("working!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Applicaion())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

