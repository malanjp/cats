# -*- coding: utf-8 -*-
from cats import Cats, BaseSocketIO, render_template, WSGIHandler
from webob import Request


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


def test_create_instance_settings():
    cats = Cats('notfoundsettings')
    assert cats


def test_add_route():
    urls = [
            ('', ViewTest),
            ('test2', ViewTest2),
            (r'^$', ViewTest),
            (r'^test2/$', ViewTest2),
           ]

    cats = Cats()
    assert cats.routes(urls) == None


def test_add_socketio_route():
    urls = [
            ('/', ViewTestSocketIO),
           ]

    cats = Cats()
    assert cats.socketio_routes(urls) == None


def test_call_wsgihandler():
    urls = [
            (r'^$', ViewTest),
            (r'^test2$', ViewTest2),
           ]
    req = Request.blank('/')
    res = req.call_application(WSGIHandler(urls))
    assert res

    req = Request.blank('test2')
    res = req.call_application(WSGIHandler(urls))
    assert res


def test_render_template():
    assert render_template('index.jinja') != None


