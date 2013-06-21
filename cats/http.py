# -*- coding: utf-8 -*-

class HTTPRequest(object):
    def __init__(self, environ, encoding, options):
        self.environ = environ
        self.encoding = encoding
        self.options = options
        self.method = environ['REQUEST_METHOD']

#    @attribute
    def host(self):
        host = self.environ['HTTP_HOST']
        if ',' in host:
            host = host.rsplit(',', 1)[-1].strip()
        return host

#    @attribute
    def remote_addr(self):
        addr = self.environ['REMOTE_ADDR']
        if ',' in addr:
            addr = addr.split(',', 1)[0].strip()
        return addr

#    @attribute
    def root_path(self):
        return self.environ['SCRIPT_NAME'] + '/'

#    @attribute
    def path(self):
        return self.environ['SCRIPT_NAME'] + self.environ['PATH_INFO']

#    @attribute
    def query(self):
        return parse_qs(
            self.environ['QUERY_STRING'],
            encoding=self.encoding
        )

#    @attribute
    def form(self):
        form, self.files = self.load_body()
        return form

#    @attribute
    def files(self):
        self.form, files = self.load_body()
        return files

#    @attribute
    def cookies(self):
        if 'HTTP_COOKIE' in self.environ:
            return parse_cookie(self.environ['HTTP_COOKIE'])
        else:
            return {}

#    @attribute
    def ajax(self):
        if 'HTTP_X_REQUESTED_WITH' in self.environ:
            return self.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'
        else:
            return False

#    @attribute
    def secure(self):
        return self.environ['wsgi.url_scheme'] == 'https'

#    @attribute
    def scheme(self):
        return self.environ['wsgi.url_scheme']

#    @attribute
    def urlparts(self):
        return UrlParts((self.scheme, self.host,
                         self.path, self.environ['QUERY_STRING'], None))

    def load_body(self):
        """ Load http request body and returns
            form data and files.
        """
        environ = self.environ
        cl = environ['CONTENT_LENGTH']
        icl = int(cl)
        if icl > self.options['MAX_CONTENT_LENGTH']:
            raise ValueError('Maximum content length exceeded')
        fp = environ['wsgi.input']
        ct = environ['CONTENT_TYPE']
        if ct.startswith('m'):
            return parse_multipart(fp, ct, cl, self.encoding)
        else:
            qs = bton(fp.read(icl), self.encoding)
            return parse_qs(qs, self.encoding), None


class HTTPResponse(object):
    """ HTTP response.

        Response headers Content-Length and Cache-Control
        must not be set by user code directly. Use
        ``HTTPCachePolicy`` instead (``HTTPResponse.cache``).
    """
    status_code = 200
    cache_policy = None
    cache_profile = None

    def __init__(self, content_type='text/html; charset=UTF-8',
                 encoding='UTF-8'):
        """ Initializes HTTP response.
        """
        self.content_type = content_type
        self.encoding = encoding
        self.headers = [('Content-Type', content_type)]
        self.buffer = []
        self.cookies = []
        self.cache_dependency = []

    def get_status(self):
        """ Returns a string that describes the specified
            HTTP status code.
        """
        return HTTP_STATUS[self.status_code]

    status = property(get_status)

    def redirect(self, absolute_url, status_code=302):
        """ Redirect response to ``absolute_url`` and sets
            ``status_code``.
        """
        self.status_code = status_code
        self.headers.append(('Location', absolute_url))

    def write(self, chunk):
        """ Applies encoding to ``chunk`` and append it to response
            buffer.
        """
        self.buffer.append(chunk.encode(self.encoding))

    def write_bytes(self, chunk):
        """ Appends chunk it to response buffer. No special checks performed.
            It must be valid object for WSGI response.
        """
        self.buffer.append(chunk)

    def __call__(self, start_response):
        """ WSGI call processing.
        """
        headers = self.headers
        append = headers.append
        cache_policy = self.cache_policy
        if cache_policy:
            cache_policy.extend(headers)
        else:
            append(HTTP_HEADER_CACHE_CONTROL_DEFAULT)
        if self.cookies:
            encoding = self.encoding
            for cookie in self.cookies:
                append(cookie.http_set_cookie(encoding))
        buffer = self.buffer
        append(('Content-Length', str(sum([len(chunk) for chunk in buffer]))))
        start_response(HTTP_STATUS[self.status_code], headers)
        return buffer



