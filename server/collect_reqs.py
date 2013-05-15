from tornado.escape import native_str, parse_qs_bytes, utf8
from tornado import httputil
import tornado.httpserver
from tornado.log import gen_log
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import hashlib

from myconfigparser import get_list
from tornado.httpserver import _BadRequestException
from tornado.options import define, options
define("port", default=8080)


def parse_request(data):
    try:
        data = native_str(data.decode('latin1'))
        eol = data.find("\r\n")
        eol2 = data.find("\r\n\r\n")
        start_line = data[:eol]
        get_arguments = {}
        post_arguments = {}
        files = {}
        try:
            method, uri, version = start_line.split(" ")
        except ValueError:
            raise _BadRequestException("Malformed HTTP request line")
        if not version.startswith("HTTP/"):
            raise _BadRequestException("Malformed HTTP version")
        try:
            headers = httputil.HTTPHeaders.parse(data[eol:eol2])
        except ValueError:
            raise _BadRequestException("Malform HTTP headers")

        content_length = headers.get("Content-Length")
        host = headers.get("Host")
        content_type = headers.get("Content-Type", "")
        path, sep, query = uri.partition('?')
        get_arguments = parse_qs_bytes(query, keep_blank_values=True)
        if content_length:
            body = data[eol2:].strip()
            httputil.parse_body_arguments(
                content_type, body, post_arguments, files)
            return host, path, get_arguments, post_arguments, files
        return host, path, get_arguments, {}, {}
    except _BadRequestException as e:
        gen_log.info("Malformed HTTP request:%s", e)
        return


def gen_uniqcode(host, path, get_arg, post_arg, files):
        MVC_PARAMS = get_list('config.ini', 'MVC Params', 'paramList')
        args = {}
        args.update(get_arg)
        args.update(post_arg)
        args.update(files)
        keys = ''
        for key in sorted(args.iterkeys()):
            if key in MVC_PARAMS:
                key += '=' + args[key][0]
            keys += key
            keys += '&'
        uniq_qry = host + path + keys
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
        host, path, get_arg, post_arg, files = parse_request(req)
        uniq_code = gen_uniqcode(host, path, get_arg, post_arg, files)
        #self.db.insert({md5:uniq_code, domain:host,request:req})
        self.db.requests.insert({"_id":uniq_code, "domain":host,"request":req})
        self.write(uniq_code)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("working!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Applicaion())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
