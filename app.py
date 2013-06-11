# -*- coding: utf-8 -*-
from cats.base import CatsHttpBase

cats = CatsHttpBase()
httpd = cats.make_server('', 8000, cats)
print("Serving on port 8000...")
httpd.serve_forever()


