# -*- coding: utf-8 -*-
from cats import Cats, BaseHandler, HTTPResponse, WSGIApplication

#cats = Cats()
#
#def Test(BaseHandler):
#    def get(self):
#        return self.render_template('templates/index.html')
#
#
#urls = [
#    url(path='/test', controller=Test, name='test'),
#]
#
#app = WSGIApplication(urls=urls, options={'encoding':'utf-8'})
#
#httpd = app.run('0.0.0.0', 8000, app)
#print("Serving on port 8000...")


if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description='Echo gevent Server')
    parser.add_argument('--host', default='192.168.72.100')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = WSGIServer((args.host, args.port), EchoWebSocketApplication(args.host, args.port))
    server.serve_forever()


