# -*- coding: utf-8 -*-
from base import CatsHttpBase

cats = CatsHttpBase()
httpd = cats.make_server('', 8000)
print("Serving on port 8000...")
httpd.serve_forever()


