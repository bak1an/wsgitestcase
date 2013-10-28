import requests
import socket
from wsgitestcase import WsgiTestCase, WsgiThread
from wsgitestcase import get_cool_unittest
from werkzeug.wrappers import Request, Response


unittest = get_cool_unittest()


@Request.application
def goodbye_app(request):
    return Response("goodbye world")


class TestSimpleServer(WsgiTestCase):

    def test_simpleserver(self):
        r = requests.get("http://%s:%s/" % (self.host, self.port))
        self.assertEqual(r.text, "hello world")


class TestOtherApp(WsgiTestCase):

    app = staticmethod(goodbye_app)

    def test_simpleserver(self):
        r = requests.get("http://%s:%s/" % (self.host, self.port))
        self.assertEqual(r.text, "goodbye world")


class TestPortsRange(unittest.TestCase):

    def setUp(self):
        self.open_sockets = []
        self.addCleanup(self.cleanup_sockets)

    def cleanup_sockets(self):
        for s in self.open_sockets:
            s.close()

    def listen_on(self, port):
        pass

    def test_nobusy(self):
        self.t = WsgiThread(goodbye_app)
        self.assertIsNone(self.t.port)
        self.t.start()
        self.t.up_and_ready.wait()
        self.addCleanup(self.t.join)
        self.assertEqual(self.t.port, 8000)


if __name__ == '__main__':
    unittest.main()
