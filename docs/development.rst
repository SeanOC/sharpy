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


