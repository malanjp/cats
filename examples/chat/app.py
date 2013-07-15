# -*- coding: utf-8 -*-
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, '../..'))
from cats import Cats, BaseSocketIO, render_template
import argparse
import random

app = Cats()


class ViewTest:
    def get(self, request):
        return render_template('index.jinja', \
            {
             'username': random.randint(0, 100),
             'host': args.host,
             'port': args.port
            })

    def post(self, request):
        #print(request.POST.get('post-msg'))
        return 'you sent message: %s' % request.POST.get('post-msg')


class ViewTest2:
    def get(self, request):
        return 'Test2 hogehoge'


class ViewTestSocketIO(BaseSocketIO):
    def on_nickname(self, nickname):
        if not self.request['box'].get('nicknames'):
            self.request['box']['nicknames'] = []

        self.request['box']['nicknames'].append(nickname)
        self.socket.session['nickname'] = nickname
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.request['box']['nicknames'])
        self.join('main_room')

    def recv_disconnect(self):
        nickname = self.socket.session['nickname']
        self.request['box']['nicknames'].remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.request['box']['nicknames'])

        self.disconnect(silent=True)

    def on_user_message(self, msg):
        self.emit_to_room('main_room', 'msg_to_room',
            self.socket.session['nickname'], msg)


# defining route
urls = [
        ('/', ViewTest), # call 'get' method from Test class
        ('/test2', ViewTest2), # call 'get' method from Test class
       ]
socketio_urls = [
        ('/', ViewTestSocketIO), # call 'get' method from Test class
       ]

app.routes(urls)
app.socketio_routes(socketio_urls)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Echo gevent Server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = app.run(args.host, args.port)
    server.serve_forever()


