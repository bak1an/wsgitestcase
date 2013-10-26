import os

from setuptools import setup

DESCRIPTION = ""
with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
    DESCRIPTION = f.read()

setup(
    name="wsgitestcase",
    version="0.1",
    author="Anton Baklanov",
    author_email="antonbaklanov@gmail.com",
    license="MIT",
    url="",
    py_modules=["wsgitestcase"],
    install_requires=["Werkzeug==0.9.4"],
    description="TestCase that will launch your wsgi/werkzeug application in a separate thread for you",
    long_description=DESCRIPTION,
    classifiers=[]
)

