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
    packages="",
    description="",
    long_description=DESCRIPTION,
    classifiers=[]
)

