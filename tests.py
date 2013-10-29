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


class TestPortSelect(unittest.TestCase):

    def setUp(self):
        self.open_sockets = []
        self.threads = []
        self.addCleanup(self.cleanup)

    def cleanup(self):
        for s in self.open_sockets:
            s.close()
        for t in self.threads:
            t.join()

    def listen_on(self, port):
        pass

    def test_one_server(self):
        t = WsgiThread(goodbye_app)
        self.threads.append(t)
        self.assertIsNone(t.port)
        t.start()
        t.up_and_ready.wait()
        self.assertEqual(t.port, 8000)

    def test_two_servers(self):
        t1 = WsgiThread(goodbye_app)
        t2 = WsgiThread(goodbye_app)
        self.threads.append(t1)
        self.threads.append(t2)
        t1.start()
        t2.start()
        t1.up_and_ready.wait()
        t2.up_and_ready.wait()
        self.assertEqual(t1.port, 8000)
        self.assertEqual(t2.port, 8001)


if __name__ == '__main__':
    unittest.main()
