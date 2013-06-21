# -*- coding: utf-8 -*-
from template import render_template


class BaseHandler(object):
    def render_template(self, filename):
        ret = render_template(filename)
        return ret

    def render_renponse(self, obj):
        response = HttpResponse()

