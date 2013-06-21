# -*- coding: utf-8 -*-
from http import HTTPResponse, HTTPRequest
from webob import Request, Response

class WSGIApplication(object):
    def __call__(self, environ, start_response):
        """ WSGI application entry point.
        """
        request = HTTPRequest(environ, self.encoding, self.options)
        print(request)
        response = self.middleware(request)
        if response is None:
            response = not_found()
        return response(start_response)

    def dispatch(self, request):
        print(request)
        pass

    def wsgi_app(self, environ, start_response):
        request = webob.Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)

    def run(self, address='localhost', port=8000, app=None):
        try:
            server = SocketIOServer((address, port), app,
                    resource="socket.io", policy_server=True,
                    policy_listener=(address, 10843))
            #server = SocketIOServer(app,
            #        resource="socket.io", policy_server=True,
            #        policy_listener=(address, 10843))
            print "Server running on port %s:%d. Ctrl+C to quit" % (address, port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
            print "Bye bye"


    def url(self, path, controller, **kwargs):
        if isinstance(controller, BaseHandler):
            print('controller is BaseHandler instance')
        pass

