import SocketServer
class StreamServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True
    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address)

def proxy_handler(sock, address):
    reqfile = sock.makefile('rb', 8192)
    try:
        method, path, version, headers = http.parse_request(reqfile)
    except (EOFError, socket.error) as e:
        if e[0] in ('empty line', 10053, errno.EPIPE):
            return reqfile.close()
        raise

    remote_addr, remote_port = address

    __realsock = None
    __realreqfile = None

    host = headers.get('Host', '')
    if path[0] == '/' and host:
        path = 'http://%s%s' % (host, path)

    try:
        try:
            content_length = int(headers.get('Content-Length', 0))
            payload = reqfile.read(content_length) if content_length else ''
            urlfetch = paas_urlfetch
            appcode, code, resp_hdr, resp_file = urlfetch(method, path, headers, payload)
            logging.info('%s:%s "%s %s HTTP/1.1" %s -' % (remote_addr, remote_port, method, path, code))
        except socket.error as e:
            if e.reason[0] not in (11004, 10051, 10060, 'timed out', 10054):
                raise
        except Exception as e:
            logging.exception('error: %s', e)
            raise

        if appcode in (400, 405):
            http.crlf = 0

        wfile = sock.makefile('wb', 0)
        http.copy_resp(code, resp_hdr, write=wfile.write)
        http.copy_body(resp_file, resp_hdr, write=wfile.write)
        resp_file.close()

    except socket.error as e:
        if e[0] not in (10053, errno.EPIPE):
            raise

    finally:
        reqfile.close()
        sock.close()
        if __realreqfile:
            __realreqfile.close()
        if __realsock:
            __realsock.close()


def main():
    server = StreamServer(("127.0.0.1", 8080), proxy_handler)
    server.serve_forever()

if '__main__' == __name__:
    main()