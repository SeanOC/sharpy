==============
High Level API
==============

Sharpy's high level API provides a nice pythonic interface for working with 
the Cheddar Getter API.  While there are some variations to make things a 
bit nicer to work with in Python, most of the methods below map pretty 
directly.  If you are looking for more detail on what exactly an API call does
or what exactly a particular value means in a given context, you should look
at the `Cheddar Getter API Docs <https://cheddargetter.com/developers>`_.

For the most part, sharpy's high level API presents itself as a collection of 
classes/objects which map to logical entities in the Cheddar Getter API.  Below are details on those classes and some examples of their use.

.. py:currentmodule:: sharpy.product

~~~~~~~~~~~~~~
CheddarProduct
~~~~~~~~~~~~~~

.. autoclass:: CheddarProduct
    
    CheddarProduct is the core of Sharpy's high level API, much like the 
    product entity is the core of the Cheddar Getter API.  This will be the 
    object which keeps track of your credentials and provides you with access
    to the rest of the API.
    
    :param username: Your Cheddar Getter Username
    :param password: Your Cheddar Getter Password
    :param product_code: Your Cheddar Getter Product Code
    :param cache: Either a file system path or an objects which implements the `httplib2 cache API <http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html#id2>`_ to be used for caching of HTTP responses
    :param timeout: The socket level timeout for HTTP requests.
    :param endpoint: The URL for an alternate API endpoint for Sharpy to use.
    
    .. automethod:: get_all_plans
    
    Returns all of the plans available for the product
    
    .. automethod:: get_plan
    
    Returns the plan with the provided code.
    
    :param code: The code for the desired plan.
    
    .. automethod:: create_customer
    
    Creates a customer 
    
