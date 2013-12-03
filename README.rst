    :VERSION: 0.1

.. image:: https://travis-ci.org/bak1an/wsgitestcase.png?branch=master
   :target: https://travis-ci.org/bak1an/wsgitestcase

TestCase that will launch your wsgi/werkzeug application in a separate thread
for you (using *setUp* and *tearDown* methods).

Inspired by Django's LiveServerTestCase.

How to
------

.. code:: python

   import requests  # you should use this, requests is cool
   from wsgitestcase import WsgiTestCase

   class MyTestCase(WsgiTestCase):

       # add your wsgi application here
       # you can also set it with something like
       # app = staticmethod(my_wsgi_app)
       # see tests.py for more examples
       @staticmethod
       def app(environ, start_response):
           start_response('200 OK', [('Content-Type', 'text/plain')])
           yield 'Hello World'

       def test_something(self):
           # server with your app should be already up
           # use self.host, self.port and self.url to find out where it is
           r = requests.get("http://%s:%s/" % (self.host, self.port))
           self.assertEqual(r.text, "Hello World")
           # in self.requests you can find a list with all requests made to
           # your app. it contains werkzeug's Request objects.
           # see tests.py for more examples
           # and werkzeug's doc at http://werkzeug.pocoo.org/docs/wrappers/
           # for Request object reference
           self.assertEqual(len(self.requests), 1)
           self.assertEqual(self.requests[0].path, "/")


License
-------

wsgitestcase is distributed under terms of MIT license.
