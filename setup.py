import os
import platform

from setuptools import setup

dependencies = ["Werkzeug==0.9.4"]

if platform.python_version() < '2.7':
    dependencies.append("unittest2")

DESCRIPTION = ""
with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
    DESCRIPTION = f.read()

setup(
    name="wsgitestcase",
    version="0.1",
    author="Anton Baklanov",
    author_email="antonbaklanov@gmail.com",
    license="MIT",
    url="https://github.com/bak1an/wsgitestcase",
    py_modules=["wsgitestcase"],
    install_requires=dependencies,
    description="TestCase that will launch your wsgi/werkzeug application in a separate thread for you",
    long_description=DESCRIPTION,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing"
    ]
)

