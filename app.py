# -*- coding: utf-8 -*-
import cats
from cats import Cats, render_template
import argparse
import random

app = Cats()


class ViewTest:
    def get(self, request):
        return render_template('index.jinja', {
                                               'username': random.randint(0, 100),
                                               'host': args.host,
                                               'port': args.port
                                              })

    def post(self, request):
        return 'called post method.'


class ViewTest2:
    def get(self, request):
        return 'Test2 hogehoge'


## mock url
urls = [
        ('/', ViewTest), # call 'get' method from Test class
        ('/test2', ViewTest2), # call 'get' method from Test class
       ]

app.routes(urls)


if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description='Echo gevent Server')
    parser.add_argument('--host', default='192.168.72.100')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = app.run(args.host, args.port)
    server.serve_forever()


