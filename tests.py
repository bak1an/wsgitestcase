import requests
from wsgitestcase import WsgiTestCase
from wsgitestcase import get_cool_unittest

unittest = get_cool_unittest()


class TestSimpleServer(WsgiTestCase):

    def test_simpleserver(self):
        r = requests.get("http://%s:%s/" % (self.host, self.port))
        self.assertEqual(r.text, "hello world")


if __name__ == '__main__':
    unittest.main()
