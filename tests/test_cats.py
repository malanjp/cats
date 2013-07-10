# -*- coding: utf-8 -*-
import os, sys
from cats import Cats, BaseSocketIO, render_template


class ViewTest:
    def get(self, request):
        return 'ViewTest called get method.'

    def post(self, request):
        return 'ViewTest called post method.'


class ViewTest2:
    def get(self, request):
        return 'Test2 called get method.'

    def post(self, request):
        return 'ViewTest called post method.'


class ViewTestSocketIO(BaseSocketIO):
    def on_nickname(self, nickname):
        pass

    def recv_disconnect(self):
        self.disconnect(silent=True)


def test_create_instance():
    cats = Cats()
    assert cats

def test_add_route():
    urls = [
            ('/', ViewTest),
            ('/test2', ViewTest2),
           ]

    cats = Cats()
    assert cats.routes(urls) == None

def test_add_socketio_route():
    urls = [
            ('/', ViewTestSocketIO),
           ]

    cats = Cats()
    assert cats.socketio_routes(urls) == None

def test_render_template():
    assert render_template('index.jinja') != None


