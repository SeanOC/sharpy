.. Sharpy documentation master file, created by
   sphinx-quickstart on Thu Jan  6 17:10:42 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======
Sharpy
======

Sharpy is a client for the Cheddar Getter (https://cheddargetter.com/) API.
Cheddar Getter is a great service for handling recurring and usage based
billing.

There are some existing python Cheddar Getter clients but they have
significant licensing problems, packaging problems, bugs, and are only partial
implementations of the Cheddar Getter API.

Sharpy offers a number of advantages:

* Clear and simple BSD license.
* Both a high and low level API - Work with cheddar the way you want to.
* 100% test coverage.
* Proper packaging - Sharpy can be installed via easy_install and PIP.
* Implements almost all of the Cheddar Getter API (See TODOs below).
* Will have complete documentation soon.

That all being said, sharpy is still very new and is likely to undergo some 
significant API changes in the near future.  The code should be fairly safe 
to use as long as you understand that future releases may not be backwards 
compatible.

Getting Started
===============

To get started with Sharpy, simply install it like you would any other python
package

   pip install sharpy

Optionally, you can also install `lxml <http://codespeak.net/lxml/>`_ on your
system for faster XML parsing.

Once you have sharpy installed, checkout our `docs <http://sharpy.readthedocs.org>`_
on how to use the library.

Get the documentation
=====================

Sharpy's documentation is available at `ReadTheDocs
<http://sharpy.readthedocs.org>`_ or in the ``docs`` directory of the project.

Code
====

You can checkout and download Sharpy's latest code at `Github
<https://github.com/saaspire/sharpy>`_.

TODOs
=====

* Flesh out the documentation to cover the full API.
* Add support for the various filtering options in the `get_customers` call.

=============
Documentation
=============

.. toctree::
   :maxdepth: 1
   
   examples
   high_level_api
   development

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

