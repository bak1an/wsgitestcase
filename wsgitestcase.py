import threading
import errno
import platform
import socket

from wsgiref.simple_server import make_server
from wsgiref.simple_server import WSGIRequestHandler
from wsgiref.simple_server import WSGIServer

from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware


def get_cool_unittest():
    if platform.python_version() < '2.7':
        try:
            return __import__('unittest2')
        except ImportError:
            print("Not enough unittest2")
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


class ResourceFairServer(WSGIServer):

    def server_bind(self):
        try:
            WSGIServer.server_bind(self)  # old-style classes here
        except socket.error:
            self.socket.close()
            raise


class WsgiThread(threading.Thread):

    def __init__(self, app, **kwargs):
        self.app = app
        self.host = "127.0.0.1"
        self.port = None
        self.ports_range = range(8000, 8010)
        self.up_and_ready = threading.Event()
        self.error = None
        self.server = None
        super(WsgiThread, self).__init__(**kwargs)

    def run(self):
        for i, p in enumerate(self.ports_range):
            try:
                self.server = make_server(self.host, p, self.app,
                                          handler_class=SilentRequestHandler,
                                          server_class=ResourceFairServer)
                self.port = p
                break
            except socket.error as e:
                if hasattr(e, 'errno') and e.errno == errno.EADDRINUSE:
                    if i < (len(self.ports_range) - 1):
                        continue
                self.error = e
                self.up_and_ready.set()
                return
        self.up_and_ready.set()
        self.server.serve_forever()

    def join(self):
        self.server.shutdown()
        self.server.server_close()
        super(WsgiThread, self).join()


class WsgiTestCase(unittest.TestCase):

    app = staticmethod(helloworld_app)

    @classmethod
    def setUpClass(cls):
        cls.server_thread = WsgiThread(cls.app)
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
