#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Sharpy',
    version='0.6.5',
    description='Python client for the Cheddar Getter API (http://cheddargetter.com).',
    author="Sean O'Connor",
    author_email="sean@saaspire.com",
    url="https://github.com/Saaspire/sharpy",
    packages=['sharpy'],
    license="BSD",
    long_description=open('README.rst').read(),
    install_requires=['httplib2', 'elementtree', 'python-dateutil'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)