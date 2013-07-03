# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import argparse
import random
import os

import gevent
import gevent.pywsgi

from ws4py.server.geventserver import WebSocketWSGIApplication, \
     WebSocketWSGIHandler, WSGIServer
from ws4py.websocket import EchoWebSocket


class BroadcastWebSocket(EchoWebSocket):
    def opened(self):
        app = self.environ['ws4py.app']
        app.clients.append(self)
        print('ws opend')

    def received_message(self, m):
        # self.clients is set from within the server
        # and holds the list of all connected servers
        # we can dispatch to
        app = self.environ['ws4py.app']
        for client in app.clients:
            print(m)
            client.send(m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        print('ws closed')
        app = self.environ.pop('ws4py.app')
        if self in app.clients:
            app.clients.remove(self)
            for client in app.clients:
                try:
                    client.send(reason)
                except:
                    pass


class WebSocketHandler:
    def favicon(self, environ, start_response):
        """
        Don't care about favicon, let's send nothing.
        """
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return ""

    def webapp(self, environ, start_response):
        """
        Our main webapp that'll display the chat form
        """
        status = '200 OK'
        headers = [('Content-type', 'text/html')]

        start_response(status, headers)
        return "this is a WebSocketHandler class."


class Dispatcher:
    def __init__(self, host, port, url_list):
        self.host = host
        self.port = port
        self.ws = WebSocketWSGIApplication(handler_cls=BroadcastWebSocket)
        self.url_list = url_list

        # keep track of connected websocket clients
        # so that we can brodcasts messages sent by one
        # to all of them. Aren't we cool?
        self.clients = []

    def __call__(self, environ, start_response):
        """
        Good ol' WSGI application. This is a simple demo
        so I tried to stay away from dependencies.
        """
        print(environ['PATH_INFO'])
        if environ['PATH_INFO'] == '/favicon.ico':
            return self.favicon(environ, start_response)

        if environ['PATH_INFO'] == '/ws':
            print('ws')
            environ['ws4py.app'] = self
            return self.ws(environ, start_response)

        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        print(self.url_list)
        for cls in self.url_list:
            if cls[0] == environ['PATH_INFO']:
                instance = cls[1]()
                return instance.get(environ, start_response)

        return self.webapp(environ, start_response)

    def favicon(self, environ, start_response):
        """
        Don't care about favicon, let's send nothing.
        """
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return ""

    def webapp(self, environ, start_response):
        """
        Our main webapp that'll display the chat form
        """
        status = '200 OK'
        headers = [('Content-type', 'text/html')]

        start_response(status, headers)
        return "this is a WebSocketHandler class."


class Cats:
    def routes(self, urls=None):
        self.url_list = urls
        print(urls)

    def run(self, host='localhost', port=9000):
        #TODO: app.py のクラス呼び出したい
        #server = WSGIServer((host, port), WebSocketHandler(host, port))
        server = WSGIServer((host, port), Dispatcher(host, port, self.url_list))
        server.serve_forever()


def url(pattern, handler, kwargs=None, name=None):
    """ Converts parameters to tupple of length four.
        Used for convenience to name parameters and skip
        unused.
    """
    return pattern, handler, kwargs, name


if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description='Echo gevent Server')
    parser.add_argument('--host', default='192.168.72.100')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = WSGIServer((args.host, args.port), WebSocketHandler(args.host, args.port))
    server.serve_forever()




