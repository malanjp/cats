# -*- coding: utf-8 -*-
from cats.base import CatsWebBase

cats = CatsWebBase()
httpd = cats.make_server('', 8000, cats)
print("Serving on port 8000...")


