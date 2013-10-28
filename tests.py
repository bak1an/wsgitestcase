import requests
from wsgitestcase import WsgiTestCase
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


if __name__ == '__main__':
    unittest.main()
