import threading
import errno
import platform
import socket

from wsgiref.simple_server import WSGIRequestHandler
from wsgiref.simple_server import WSGIServer

from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

try:
    from io import BytesIO as IO
except ImportError:
    from StringIO import StringIO as IO


def get_cool_unittest():
    if platform.python_version() < '2.7':
        try:
            return __import__('unittest2')
        except ImportError:
            raise
    else:
        return __import__('unittest')


unittest = get_cool_unittest()


@Request.application
def helloworld_app(request):
    return Response("hello world")


@Request.application
def all_404(request):
    return Response("Nothing here", status=404)


def get_static_files_app(base_path):
    return SharedDataMiddleware(all_404, {'/': base_path})


class SilentRequestHandler(WSGIRequestHandler):

    def log_request(self, code=None, size=None):
        pass

    def handle(self):
        req = self.request.recv(1024)
        if len(req) == 1024:
            self.request.settimeout(1)
            while True:
                try:
                    data = self.request.recv(1024)
                except socket.timeout:
                    data = None
                if not data:
                    break
                req += data
        self.rfile = IO(req)
        WSGIRequestHandler.handle(self)


class ResourceFairServer(WSGIServer):

    def server_bind(self):
        try:
            WSGIServer.server_bind(self)  # old-style classes here
        except socket.error:
            self.socket.close()
            raise


class LoggingMiddleware(object):

    def __init__(self, app, request_lists):
        self.app = app
        self.request_lists = request_lists

    def __call__(self, environ, start_response):
        environ_clone = environ.copy()
        data_position = environ['wsgi.input'].tell()
        environ_clone['wsgi.input'] = IO(environ['wsgi.input'].read())
        environ['wsgi.input'].seek(data_position)
        req = Request(environ_clone)
        for lst in self.request_lists:
            lst.append(req)
        return self.app(environ, start_response)


class WsgiThread(threading.Thread):

    def __init__(self, app, **kwargs):
        self.app = app
        self.host = "127.0.0.1"
        self.port = None
        self.ports_range = range(8000, 8010)
        self.up_and_ready = threading.Event()
        self.error = None
        self.server = None
        self.request_lists = []
        super(WsgiThread, self).__init__(**kwargs)

    def run(self):
        for i, p in enumerate(self.ports_range):
            try:
                self.server = ResourceFairServer((self.host, p),
                                                 SilentRequestHandler)
                self.server.set_app(
                    LoggingMiddleware(self.app, self.request_lists))
                self.port = p
                break
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    if i < (len(self.ports_range) - 1):
                        continue
                self.error = e
                self.up_and_ready.set()
                return
            except:
                self.up_and_ready.set()
                raise
        self.up_and_ready.set()
        self.server.serve_forever()

    def join(self):
        self.server.shutdown()
        self.server.server_close()
        super(WsgiThread, self).join()

    def log_requests(self, lst):
        self.request_lists.append(lst)


class WsgiTestCase(unittest.TestCase):

    app = staticmethod(helloworld_app)

    def setUp(self):
        self.requests = []
        self.server_thread.log_requests(self.requests)

    @classmethod
    def setUpClass(cls):
        cls.server_thread = WsgiThread(cls.app)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.server_thread.up_and_ready.wait()
        if cls.server_thread.error:
            raise cls.server_thread.error
        cls.host = cls.server_thread.host
        cls.port = cls.server_thread.port
        cls.url = "http://%s:%s/" % (cls.host, cls.port)

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.join()
