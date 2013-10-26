import threading
import unittest
import time
import errno

from wsgiref.simple_server import make_server

from werkzeug.wrappers import Request, Response


@Request.application
def helloworld_app(request):
    return Response("hello world")


class WsgiThread(threading.Thread):

    def __init__(self, app, **kwargs):
        self.app = app
        self.port = 8000
        self.host = "127.0.0.1"
        self.up_and_ready = threading.Event()
        self.error = None
        super(WsgiThread, self).__init__(**kwargs)

    def run(self):
        self.server = make_server(self.host, self.port, self.app)
        self.up_and_ready.set()
        self.server.serve_forever()

    def join(self):
        self.server.shutdown()
        super(WsgiThread, self).join()


class WsgiTestCase(unittest.TestCase):

    app = helloworld_app

    @classmethod
    def setUpClass(cls):
        cls.server_thread = WsgiThread(cls.app)
        cls.server_thread.start()
        cls.server_thread.up_and_ready.wait()
        cls.host = cls.server_thread.host
        cls.port = cls.server_thread.port
        if cls.server_thread.error:
            raise cls.server_thread.error

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.join()

