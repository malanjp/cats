# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer

class Cats(object):
    def __init__(self):
        pass

    def run(self, address='localhost', port=8000, app=None):
        try:
            server = SocketIOServer((address, port), app,
                    resource="socket.io", policy_server=True,
                    policy_listener=(address, 10843))
            print "Server running on port %s:%d. Ctrl+C to quit" % (address, port)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()
            print "Bye bye"


class BaseHandler(object):
    def render_template(self, filename):
        ret = render_template(filename)
        return ret

    def render_renponse(self, obj):
        response = HttpResponse()






