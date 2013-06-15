# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer

class CatsWebBase(object):
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)

        ret = [("%s: %s\n" % (key, value)).encode("utf-8")
               for key, value in environ.items()]
        #ret = []
        return ret

    def make_server(self, address='localhost', port=8000, app=None):

        #server = WSGIServer((address, port), app, log=None)
        try:
            server = SocketIOServer((address, port), app,
                    resource="socket.io", policy_server=True,
                    policy_listener=('0.0.0.0', 10843))
            print "Server running on port %s:%d. Ctrl+C to quit" % (address, port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
            print "Bye bye"


class CatsSocketIoBase(object):
    pass



