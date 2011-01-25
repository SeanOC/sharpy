.. py:currentmodule:: sharpy.product

~~~~~~~~
Examples
~~~~~~~~

Below are a series of examples of how to do common tasks using sharpy.

---------
Customers
---------


========
Creation
========

Customer creation is generally just a simple call on a product instance.  The 
:py:func:`CheddarProduct.create_customer` method supports everything that the Cheddar Getter API 
`add customer <https://cheddargetter.com/developers#add-customer>`_ call
supports.

Free Customers
==============

Free customers require a minimal amount of information.  Accordingly, the call to create them is pretty simple.

.. literalinclude:: examples/customer_creation/free.py
    :linenos:

Paid Customers
==============

Paid customers require a bit more information, but still are fairly easy to create.

.. literalinclude:: examples/customer_creation/paid.py
    :linenos:

Customers With Optional Info
============================

Cheddar has a number of optional fields which they accept when creating a
customer.  Most of these fields are simply provided to help you keep track
of customer info, but some of the fields (e.g. ``initial_bill_date``) can
affect Cheddar Getter's behavior.  Check out Cheddar Getter's `API docs  <https://cheddargetter.com/developers#add-customer>`_ for more details on specific optional fields.

.. literalinclude:: examples/customer_creation/optional.py
    :linenos:
    
.. note::

    Notice that the initial_bill_date is provided as a :py:class:`datetime`
    object. Sharpy always expects and returns the best python native data
    structure for a given piece of information.  That being said, sharpy is
    generally pretty flexible about what forms of data it will take in.


Customers With Tracked Items
============================

Depending on your pricing model, you may want to create customers as having
already consumed `tracked items
<http://support.cheddargetter.com/kb/pricing-plans/pricing-plan-basics>`_.
Fortunately, Cheddar Getter's API allows us to provide tracked item
information as part of the create customer call.  While you can always
report on tracked items with their own API calls, reporting tracked item
usage as part of customer creation saves a potentially slow request/response
cycle and avoids possible error states where a create customer call succeeds
but subsequent API calls fail.

To create a customer with tracked item information, all you need to do is pass
in a collection of dictionaries to the ``items`` parameter of the
:py:func:`CheddarProduct.create_customer` which describe the desired
item info.

.. literalinclude:: examples/customer_creation/items.py
    :linenos:
    
Notice here that the ``quantity`` value of the item dictionary is optional. 
If you don't include a ``quantity`` value, sharpy assumes a quantity of ``1``.

Customers With Custom Charges
=============================

Similar to creating customers with tracked items, the Cheddar Getter API
allows you to provide custom charge information as part of the create customer
call.  Doing so saves a request to the API and eliminates the risk of 
customers getting created without the desired charges.  Just like with
tracked items, you provide charge information by building a collection
of dictionaries and passing that collection to the ``charges`` parameter
of :py:func:`CheddarProduct.create_customer`.

.. literalinclude:: examples/customer_creation/charges.py
    :linenos:
    
A few things to notice here:

    * Quantity is optional and will be assumed to be ``1`` if not provided.
    * Description is optional and will be assumed to be ``""``.
    * Each amount can be of any type which can be cast to 
      `Decimal <http://docs.python.org/library/decimal.html>`_.
    * Negative values for ``each_amount`` are credits to the customer's
      account, positive values are charges.
      

========
Fetching
========

Get an individual customer
==========================

To fetch the information for an individual customer, simply call 
:py:func:`CheddarProduct.get_customer` with your customer's code. The
customer's code is the unique identifier you provided in your customer
creation call.

.. literalinclude:: examples/customer_fetch/get_customer.py

If a customer with the given code cannot be found, a 
:py:class:`sharpy.exceptions.NotFound` exception will be raised.

Get all customers
=================

.. literalinclude:: examples/customer_fetch/all_customers.py