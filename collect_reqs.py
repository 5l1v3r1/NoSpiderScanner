from tornado.escape import native_str, parse_qs_bytes, utf8
from tornado import httputil
import tornado.httpserver
from tornado.log import gen_log
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo

from tornado.httpserver import _BadRequestException
from tornado.options import define, options
define("port", default=8080)

class Md5Request(object):
    def __init__(self):
        self.data = ""
        self.method = "GET"
        self.uri = "/"
        self.version = "HTTP/1.0"
        self.get_arguments = {}
        self.post_arguments = {}
        self.headers = {}
        self.files = {}

    def parse_request(self, data):
        try:
            self.data = data
            self.data = native_str(data.decode('latin1'))
            eol = self.data.find("\r\n")
            eol2 = self.data.find("\r\n\r\n")
            start_line = self.data[:eol]
            try:
                self.method, self.uri, self.version = start_line.split(" ")
            except ValueError:
                raise _BadRequestException("Malformed HTTP request line")
            if not self.version.startswith("HTTP/"):
                raise _BadRequestException("Malformed HTTP version")
            try:
                self.headers = httputil.HTTPHeaders.parse(self.data[eol:eol2])
            except ValueError:
                raise _BadRequestException("Malform HTTP headers")

            content_length = self.headers.get("Content-Length")
            content_type = self.headers.get("Content-Type", "")
            if "?" in uri:
                qidx = uri.find("?")
                self.get_arguments = parse_qs_bytes(native_str(uri[qidx+1:]), keep_blank_value=True)
            if content_length:
                body = self.data[eol2:].strip()
                httputil.parse_body_arguments(
                        content_type, body, self.post_arguments, self.files)
        except _BadRequestException as e:
            gen_log.info("Malformed HTTP request:%s", e)
            return


class Applicaion(tornado.web.Application):

    def __init__(self):
        handlers =
            [(r"/collect", CollectHandler),
             (r"/", IndexHandler)]
        conn = pymongo.Connect("localhost", 27017)
        self.db = conn["reqs"]
        tornado.web.Application.__init__(self, handlers, debug=True)


class CollectHandler(tornado.web.RequestHandler):

    def post(self):
        user_name = self.get_argument("username", "anonymous")
        internal_ip = self.get_argument("ip", "None")
        req = self.request.arguments.get("request", [""])[0]


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("working!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Applicaion())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
