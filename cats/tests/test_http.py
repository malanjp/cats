# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from base import CatsHttpBase
import requests

def test_create_httpbase():
    cats = CatsHttpBase()
    assert cats


