# -*- coding: utf-8 -*-
from jinja2 import PackageLoader, TemplateNotFound, Environment

default_mimetype = 'text/html'

env = Environment(loader=PackageLoader('cats', 'templates'))

def render_to_string(filename, context={}):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return rendered

def render_template(filename, context={}, mimetype=default_mimetype, request=None):
    if request:
        context['request'] = request
    rendered = render_to_string(filename, context)
    return rendered



