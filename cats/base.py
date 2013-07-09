# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import argparse
import random
import os

#import gevent
#import gevent.pywsgi
#
#from ws4py.server.geventserver import WebSocketWSGIApplication, \
#     WebSocketWSGIHandler, WSGIServer
#from ws4py.websocket import EchoWebSocket

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

from webob import Request

from jinja2 import Environment, PackageLoader

from pprint import pprint


class BaseSocketIO(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_disconnect(self):
        self.disconnect(silent=True)

    def recv_message(self, message):
        print "PING!!!", message


class WSGIHandler(object):
    """
    WSGIHandler class handles the HTTP request various.
    """
    def __init__(self, url_list, socketio_url_list):
        self.url_list = url_list
        self.socketio_url_list = socketio_url_list
        self.methods = {'GET':'get', 'POST':'post'}
        self.request = {'box':{}}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if path.startswith('static/'):
            return self.static(path, start_response)

        if path.startswith("socket.io"):
            ns = self.create_namespace(environ)
            socketio_manage(environ=environ, namespaces=ns, request=self.request)
        else:
            return self.dispatch(path, environ, start_response)

    def create_namespace(self, environ):
        namespace = {}

        for cls in self.socketio_url_list:
            instance = cls[1]
            namespace[cls[0]] = instance
            if cls[0] == '/':
              namespace[''] = instance

        return namespace

    def dispatch(self, path, environ, start_response):
        if path == '':
          path = '/'

        request = Request(environ)
        for cls in self.url_list:
            if cls[0] == path:
                instance = cls[1]()
                response = getattr(instance, self.methods[request.method])(request)
                status = '200 OK'
                headers = [('Content-type', 'text/html')]
                start_response(status, headers)
                return response

        return self.http404(start_response)

    def static(self, path, start_response):
            try:
                data = open(path).read()
            except Exception:
                return self.http404(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
                content_type = "application/x-shockwave-flash"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

    def http404(self, start_response):
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

    def socketio_routes(self, socketio_urls=None):
        """
        SocketIO Routing.
        """
        self.socketio_url_list = socketio_urls
        #print(self.socketio_url_list)

    def run(self, host='localhost', port=9000):
        """
        Run http and websocket server.
        """
        print 'Listening on port %s and on port 10843 (flash policy server)' % port
        SocketIOServer((host, port), WSGIHandler(self.url_list, self.socketio_url_list),
            resource="socket.io", policy_server=True,
            policy_listener=(host, 10843)).serve_forever()





