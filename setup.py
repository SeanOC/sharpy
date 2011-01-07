#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Sharpy',
    version='0.1',
    description='Python client for the Cheddar Getter API (http://cheddargetter.com).',
    author="Sean O'Connor",
    author_email="sean@saaspire.com",
    url="https://github.com/Saaspire/sharpy",
    packages=['sharpy'],
    license="BSD",
    long_description=open('README.rst').read(),
    requires=['httplib2', 'elementtree']
)