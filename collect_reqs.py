import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8080)

class CollectHandler(tornado.web.RequestHandler):
    def get(self):
        user_name = self.get_argument("username", "anonymous")
        internal_ip = self.get_argument("ip", "None")

    def post(self):
        req = self.get_argument("req", "")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("working!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=
            [(r"/collect", CollectHandler),
             (r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
