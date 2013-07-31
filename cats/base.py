# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from webob import Request, Response
from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
import mimetypes


class BaseSocketIO(BaseNamespace, RoomsMixin, BroadcastMixin):
    """
    BaseSocketIO class handles the socketio request various.
    """
    def recv_disconnect(self):
        self.disconnect(silent=True)


class WSGIHandler(object):
    """
    WSGIHandler class handles the HTTP request various.
    """
    def __init__(self, url_list=None, socketio_url_list=None):
        self.url_list = url_list
        self.socketio_url_list = socketio_url_list
        self.request = {'box': {}}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if self.socketio_url_list and path.startswith("socket.io"):
            request = Request(environ, charset='utf8')
            ns = self.create_namespace(environ)
            socketio_manage(environ=environ,
                            namespaces=ns,
                            request=request)
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
        import re
        if path == '/':
            path = ''

        request = Request(environ, charset='utf8')
        for cls in self.url_list:
            print('path', path, cls[0])
            pattern = re.compile(cls[0])
            match = pattern.match(path)
            #if cls[0] == path:
            if match:
                instance = cls[1]()
                print(instance)
                response = getattr(instance, request.method.lower())(request)
                response = Response(body=response, charset='utf8')
                return response(environ, start_response)

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
    def __init__(self, settings=None):
        self.url_list = None
        self.socketio_url_list = None

        if settings:
            self.settings(settings)
        else:
            self.settings('settings')

    def settings(self, settings=None):
        if settings:
            try:
                self.settings = __import__(settings)
            except:
                self.settings = None

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

