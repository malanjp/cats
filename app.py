# -*- coding: utf-8 -*-
from cats import Cats, BaseHandler, HTTPResponse, WSGIApplication

cats = Cats()

def Test(BaseHandler):
    def get(self):
        return self.render_template('templates/index.html')


urls = [
    url(path='/test', controller=Test, name='test'),
]

app = WSGIApplication(urls=urls, options={'encoding':'utf-8'})

httpd = app.run('0.0.0.0', 8000, app)
print("Serving on port 8000...")



