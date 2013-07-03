# -*- coding: utf-8 -*-
import cats
from cats import WebSocketHandler, Cats
import argparse
import random

app = Cats()


class Test(WebSocketHandler):
    def get(self, environ, start_response):
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
        print(args.host, args.port)

        return """<html>
        <head>
          <script type='application/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>
          <script type='application/javascript'>
            $(document).ready(function() {

              websocket = 'ws://%(host)s:%(port)s/ws';
              if (window.WebSocket) {
                console.log('websocket');
                ws = new WebSocket(websocket);
                console.log(ws);
              }
              else if (window.MozWebSocket) {
                console.log('mozwebsocket');
                ws = MozWebSocket(websocket);
              }
              else {
                console.log('WebSocket Not Supported');
                return;
              }

              window.onbeforeunload = function(e) {
                 $('#chat').val($('#chat').val() + 'Bye bye...\\n');
                 ws.close(1000, '%(username)s left the room');

                 if(!e) e = window.event;
                 e.stopPropagation();
                 e.preventDefault();
              };
              ws.onmessage = function (evt) {
                 $('#chat').val($('#chat').val() + evt.data + '\\n');
              };
              ws.onopen = function() {
                 ws.send("%(username)s entered the room");
              };
              ws.onclose = function(evt) {
                console.log('closed');
                 $('#chat').val($('#chat').val() + 'Connection closed by server: ' + evt.code + ' \"' + evt.reason + '\"\\n');
              };

              $('#send').click(function() {
                 console.log($('#message').val());
                 ws.send('%(username)s: ' + $('#message').val());
                 $('#message').val("");
                 return false;
              });
            });
          </script>
        </head>
        <body>
        <form action='#' id='chatform' method='get'>
          <textarea id='chat' cols='35' rows='10'></textarea>
          <br />
          <label for='message'>%(username)s: </label><input type='text' id='message' />
          <input id='send' type='submit' value='Send' />
          </form>
        </body>
        </html>
        """ % {'username': "User%d" % random.randint(0, 100),
               'host': args.host,
               'port': args.port}


class Test2(WebSocketHandler):
    def get(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return 'Test2 hogehoge'


## mock url
urls = [
        ('/', Test), # call 'get' method from Test class
        ('/test2', Test2), # call 'get' method from Test class
       ]

app.routes(urls)


if __name__ == '__main__':
    from ws4py import configure_logger
    configure_logger()

    parser = argparse.ArgumentParser(description='Echo gevent Server')
    parser.add_argument('--host', default='192.168.72.100')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    server = app.run(args.host, args.port)
    server.serve_forever()


