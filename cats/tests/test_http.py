# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from base import CatsHttpBase
import requests

def test_http_server():
    cats = CatsHttpBase()
    assert cats
    httpd = cats.make_server('', 8000)
    assert httpd
#    httpd.serve_forever()
#    r = requests.get('localhost', 8000)
#    assert r.status_code == 200


