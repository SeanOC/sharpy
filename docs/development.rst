=================
Developing Sharpy
=================

Due to Sharpy's nature as an API client and due to some limitations in 
Cheddar Getter's API, there is a bit of a setup one needs to do to work
on sharpy.


~~~~~~~~~~~~~~~~~~~~~~
Cheddar Getter Account
~~~~~~~~~~~~~~~~~~~~~~

To run sharpy's test suite, you will need to create an account and product
on cheddar getter.  As part of that setup, you will need to manually create
certain plans and set certain options as they are not available to change
via Cheddar's API.


Create Account
==============

Go to the `Cheddar Getter <https://cheddargetter.com>`_ website and click on
the "sign up" link at the top right corner of the page to create account.
Their free account should give you everything you need to work on sharpy.
Once you have completed cheddar's sign-up form you will need to wait for a
confirmation email.

.. warning::

    If you already have an account, you may use that account and simply
    create a new product, but creating a separate account will protect
    you from accidentally running the test suite against and modifying
    the wrong product.
   
    
Add a Product
=============

Once you receive your confirmation email, click on the link it contains.
You should be sent to a page asking you to add a product.  What you name
your product and what you select as your product code does not matter, but
be sure to record what you set the product code to be.  You will need this
information later to configure Sharpy.  When you have completed the form,
click on "Add product" and move on to the next step.


Setup Pricing Plans
===================

Once your product is setup, you will need to setup a few pricing plans.
These plans will be used by the test suite in various ways.

.. warning::

    If you do not setup your plans exactly as described here, you may get
    false errors from the Sharpy test suite.

To get started, click on "Create Pricing Plans" on your dashboard page.
From there click on the "Add Plan" button at the top right.  Once on the
"add plan" page, fill out the form according to the information in the first
row below, and click on the "Add Plan" button at the bottom of the page. 

Once your new plan is created click on "Add Plan" at the top of the page and
repeat the process until all of the plans described below have been entered.

**Free Monthly**

:Name: Free Monthly
:Code: FREE_MONTLY
:Frequency: Monthly
:Description: A free monthly plan
:Monthly Amount: 0.00
:Charge Code: FREE_MONTHLY_RECURRING
:Setup Fee: No
:Setup Amount: 0.00
:Setup Code: FREE_MONTHLY_SETUP
:Tracked Items: *None*
:First Bill: *Leave defaults*

**Paid Monthly**

:Name: Paid Monthly
:Code: PAID_MONTHLY
:Frequency: Monthly
:Description: *None*
:Monthly Amount: 20.00
:Charge Code: PAID_MONTHLY_RECURRING
:Setup Fee: No
:Setup Amount: 0.00
:Setup Code: PAID_MONTHLY_SETUP
:Tracked Items: *None*
:First Bill: *Leave defaults*

**Tracked Monthly**

:Name: Tracked Monthly
:Code: TRACKED_MONTHLY
:Frequency: Monthly
:Description: *None*
:Monthly Amount: 10.00
:Charge Code: TRACKED_MONTHLY_AMOUNT
:Setup Fee: No
:Setup Amount: 0.00
:Setup Code: TRACKED_MONTHLY_SETUP
:Tracked Items: 

    **Monthly Item**
    
    :Name: Monthly Item
    :Code: MONTHLY_ITEM
    :Quantity Inc: 2
    :Overage Amount: 10.00
    :Monthly: Yes
    
    **Once Item**
    
    :Name: Once Item
    :Code: ONCE_ITEM
    :Quantity Inc: 0
    :Overage Amount: 10.00
    :Monthly: No



Setup Payment Gateway
=====================

After you have entered all of the pricing plans, click on the overview tab.
If you created a new cheddar account, then you don't need to do anything to
setup your payment gateway.  If you are using an existing cheddar account, 
make sure that you are setup to use Cheddar's simulator gateway.  You can
click on "Payment Gateway" to view your gateway settings.


Cheddar Plan
============

On your overview page, cheddar will prompt you to setup a paid plan.
With your production account you will almost certainly want to do this,
but for the purposes of testing Sharpy, the free plan is fine.


Configuration
=============

Again, if you have setup a new account, you should be fine running the sharpy
tests with the default cheddar settings.  If you are using an existing account 
you will want to disable all email sending.  If you do not, you will send out
a ton of garbage emails every time you run the test suite.  Additionally, you
should do everything you can to make sure that your setting match cheddar's 
default settings.  If you do not, you may get false failure while running 
sharpy's test suite.


Maintenance
===========

Congratulations!  You are done setting up your cheddar account for testing
sharpy.  Generally speaking, you shouldn't need to touch this account any
further.  The test suite should be pretty good about cleaning up after 
itself and leaving the account in the state it was in when the test run
started.  That said, if things really break you may occasionally need to log
in and clean out old/bad test data.  Similarly, future releases of sharpy 
should generally work with the data setup here, but they may occasionally
require adjustments to your cheddar account.  Should that happen, there will
be a notice in the notes for the given release.

Now you just need to setup your local environment and you'll be 
all set.


~~~~~~~~~~~~~~~~~
Local Environment
~~~~~~~~~~~~~~~~~

There is a little bit of setup you need to do to get the sharpy test suite
running on your local machine.  This setup mostly involves installing some
development/testing tools as well as configuring the test suite so that it 
knows what it needs to know about your Cheddar Getter account.


Getting the code
================

Sharpy's main repo is hosted on `Github <https://github.com/Saaspire/sharpy>`_.  The easiest way to work with the
sharpy repo will be to login to Github and make your own fork of sharpy.  
Once logged in to Github, go to the
`Sharpy <https://github.com/Saaspire/sharpy>`_ repo page and click on the
"Fork" button at the top of the page.  This will give you your own repo which
you can push code up to.  When you have any changes that you'd like to
contribute back, you can make a pull request from your repo page and we'll 
check out your change.  To get the code on to your local machine, go to your
repo page, copy the SSH or HTTP url provided at the top of the page, and then
run the command ``git clone <your repo url>``.  Git will run for a little bit
and you will have a full copy of sharpy downloaded and ready to work on.


Setting up an environment
=========================

We recommend that you work within a
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ while working on 
sharpy, but it is not required.  Working in the virtualenv makes adding and
removing packages a bit easier and it reduces possible problems caused by 
conflicting packages.  See the
`virtualenv docs <http://pypi.python.org/pypi/virtualenv>`_ for details on 
how to use virtualenv.


Add sharpy to your python path
==============================

To run the tests, sharpy must be along your python path.  There are a few 
ways to possibly accomplish this but the easiest is a .pth file.  Simply 
create a file called ``sharpy.pth`` in your site-packages directory 
(with virtualenv this will be something like 
``/path/to/your/env/lib/python2.#/site-packages/``) and put the path to your
local clone of sharpy as the contents of the file.


Install Dependencies
====================

Sharpy has a few dependencies which are normally handled by setup.py and there
are a few additional packages which the test suite depends on.  The easiest 
way to install these packages is with 
`pip <http://pypi.python.org/pypi/pip>`_.  Install pip on your system and then 
from the root of your sharpy directory, run the command 
``pip install -r dev-requirements.txt``.  This will install everything
you need.

.. warning::

    Be sure that you have activated your virtualenv before running 
    ``pip install``.  If you have not, you will install all of the dependency
    packages to your global site-packages instead of your virtualenv.
    
    
Create Config File
==================

Sharpy's test suite uses a simply ini style config file to handle your cheddar
credentials.  In the ``tests`` directory, there is a file called 
``config.ini.template``.  Copy this file to a new file called ``config.ini`` 
in your ``tests`` directory.  Once copied, open your ``config.ini`` and enter
the proper values for your cheddar account.

.. warning::

    The sharpy test suite modifies and deletes data in the cheddar 
    account/product which it is configured to work against.  Be sure that 
    you enter the credentials for your **testing** account.  If you enter
    the credentials for your real cheddar account you will end up **DELETING
    CUSTOMERS**.
    
    **DO NOT RUN THE SHARPY TEST SUITE AGAINST ANYTHING BUT A TEST ACCOUNT!**


~~~~~~~~~~~~~~~~~
Running the Tests
~~~~~~~~~~~~~~~~~

We're finally ready to run some tests!  Go into the root of your clone of
Sharpy and run the command ``nosetests``.  You should see the output of the
tests as they run and a coverage report at the end.  Sharpy's goal is to
maintain complete test coverage and any patches without appropriate, *passing*
tests will not be accepted.

Be aware that the full test suite may take a while to run as many of the test
are making actual calls to cheddar.  Relatedly, if you don't have a working
internet connection, your run of the test suite will fail.