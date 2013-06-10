# -*- coding: utf-8 -*-
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from config import debug

class CatsHttpBase(object):
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        if debug:
            setup_testing_defaults(environ)

        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)
        if debug:
            ret = [("%s: %s\n" % (key, value)).encode("utf-8")
                   for key, value in environ.items()]
        else:
            ret = []
        return ret

    def make_server(self, address='localhost', port=8000):
        return make_server(address, port, self)




