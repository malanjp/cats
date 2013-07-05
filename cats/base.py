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

from webob import Request

from jinja2 import Environment, PackageLoader

from pprint import pprint


class BroadcastWebSocket(EchoWebSocket):
    def opened(self):
        app = self.environ['catsws.app']
        app.clients.append(self)

    def received_message(self, m):
        # self.clients is set from within the server
        # and holds the list of all connected servers
        # we can dispatch to
        app = self.environ['catsws.app']
        for client in app.clients:
            print(m)
            client.send(m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        app = self.environ.pop('catsws.app')
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


class WSGIHandler:
    """
    WSGIHandler class handles the HTTP request various.
    """
    def __init__(self, host, port, url_list):
        self.host = host
        self.port = port
        self.ws = WebSocketWSGIApplication(handler_cls=BroadcastWebSocket)
        self.url_list = url_list

        self.clients = []
        self.methods = {'GET':'get', 'POST':'post'}

    def __call__(self, environ, start_response):
        """
        Good ol' WSGI application. This is a simple demo
        so I tried to stay away from dependencies.
        """
        print(environ.get('HTTP_UPGRADE'))
        if environ['PATH_INFO'] == '/favicon.ico':
            return self.favicon(environ, start_response)

        if environ.get('HTTP_UPGRADE') == 'websocket':
            environ['catsws.app'] = self
            return self.ws(environ, start_response)

        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        request = Request(environ)
        for cls in self.url_list:
            if cls[0] == environ['PATH_INFO']:
                instance = cls[1]()
                response = getattr(instance, self.methods[request.method])(request)
                status = '200 OK'
                headers = [('Content-type', 'text/html')]
                start_response(status, headers)
                return response


        return self.Http404(environ, start_response)

    def Http404(self, environ, start_response):
        status = '404 NotFound'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return "404 NotFound"

    def favicon(self, environ, start_response):
        """
        Don't care about favicon, let's send nothing.
        """
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return ""


class Cats:
    def routes(self, urls=None):
        """
        Routing.
        """
        self.url_list = urls

    def run(self, host='localhost', port=9000):
        """
        Run http and websocket server.
        """
        #TODO: app.py のクラス呼び出したい
        #server = WSGIServer((host, port), WebSocketHandler(host, port))
        server = WSGIServer((host, port), WSGIHandler(host, port, self.url_list))
        server.serve_forever()





