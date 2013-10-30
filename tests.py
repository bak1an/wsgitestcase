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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(5)
        self.open_sockets.append(s)

    def run_server_thread(self):
        t = WsgiThread(goodbye_app)
        t.start()
        t.up_and_ready.wait()
        if t.error:
            raise t.error
        self.threads.append(t)
        r = requests.get("http://%s:%s/" % (t.host, t.port))
        self.assertEqual(r.text, "goodbye world")
        return t

    def test_one_server(self):
        t = self.run_server_thread()
        self.assertEqual(t.port, 8000)

    def test_two_servers(self):
        t1 = self.run_server_thread()
        t2 = self.run_server_thread()
        self.assertEqual(t1.port, 8000)
        self.assertEqual(t2.port, 8001)

    def test_busy_ports(self):
        for port in range(8000, 8005):
            self.listen_on(port)
        t = self.run_server_thread()
        self.assertEqual(t.port, 8005)

    def test_all_ports_busy(self):
        for port in range(8000, 8010):
            self.listen_on(port)
        with self.assertRaises(socket.error):
            self.run_server_thread()

if __name__ == '__main__':
    unittest.main()
