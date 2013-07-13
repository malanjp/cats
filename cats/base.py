# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from webob import Request
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
import mimetypes


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
        self.methods = {'GET': 'get', 'POST': 'post'}
        self.request = {'box': {}}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if path.startswith("socket.io"):
            ns = self.create_namespace(environ)
            socketio_manage(environ=environ,
                            namespaces=ns,
                            request=self.request)
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
                response = getattr(instance,
                                   self.methods[request.method])(request)
                status = '200 OK'
                headers = [('Content-type', 'text/html')]
                start_response(status, headers)
                return response

        return self.static(path, start_response)

    def static(self, path, start_response):
        try:
            data = open(path).read()
        except Exception:
            return self.http404(start_response)

        mimetype, subtype = mimetypes.guess_type(path)
        start_response('200 OK', [('Content-Type', mimetype)])
        return [data]

    def http404(self, start_response):
        status = '404 NotFound'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return "404 NotFound"


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

    def run(self, host='localhost', port=9000):
        """
        Run http and websocket server.
        """
        print 'Listening on port %s and on port 10843 (flash policy server)' % port
        SocketIOServer((host, port),
                       WSGIHandler(self.url_list, self.socketio_url_list),
                       resource="socket.io", policy_server=True,
                       policy_listener=(host, 10843)).serve_forever()

