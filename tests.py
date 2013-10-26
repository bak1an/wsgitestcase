import urllib
from wsgitestcase import WsgiTestCase


class TestNothing(WsgiTestCase):

    def test_simpleserver(self):
        req = urllib.request.urlopen(
            "http://%s:%s/" % (self.host, self.port))
        self.assertEqual(req.read(), b"hello world")
