# -*- coding: utf-8 -*-
from jinja2 import FileSystemLoader, Environment

default_mimetype = 'text/html'


def load_settings(settings=None):
    return __import__(settings)

def render_to_string(filename, context={}):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return rendered

def render_template(filename, context={}, mimetype=default_mimetype, request=None):
    if request:
        context['request'] = request
    rendered = render_to_string(filename, context)
    return rendered


templates_dir = 'templates'

try:
    settings = load_settings('settings')
    try:
        getattr(settings, 'templates_dir')
        templates_dir = settings.templates_dir
    except AttributeError:
        pass
except:
    pass

env = Environment(loader=FileSystemLoader(templates_dir))


