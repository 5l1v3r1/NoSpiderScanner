import SocketServer
class StreamServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True
    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address)

def main():
    server = StreamServer(("127.0.0.1", 8080), proxy_handler)
    server.serve_forever()

if '__main__' == __name__:
    main()