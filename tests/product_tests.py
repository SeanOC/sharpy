from copy import copy
from datetime import date, datetime, timedelta
from decimal import Decimal
import unittest

from dateutil.relativedelta import relativedelta
from dateutil.tz import *
from nose.tools import raises
from testconfig import config

from sharpy.product import CheddarProduct
from sharpy.exceptions import NotFound

from testing_tools.decorators import clear_users

class ProductTests(unittest.TestCase):
    
    client_defaults =  {
        'username': config['cheddar']['username'],
        'password': config['cheddar']['password'],
        'product_code': config['cheddar']['product_code'],
    }
    
    customer_defaults = {
        'code': 'test',
        'email':'garbage@saaspire.com',
        'first_name': 'Test',
        'last_name': 'User',
        'plan_code': 'FREE_MONTHLY',
    }
    
    exipration = datetime.now() + timedelta(days=180)
    
    paid_defaults = {
        'cc_number': '4111111111111111',
        'cc_expiration': exipration.strftime('%m/%Y'),
        'cc_card_code': '123',
        'cc_first_name': 'Test',
        'cc_last_name': 'User',
        'cc_company': 'Some Co LLC',
        'cc_country': 'United States',
        'cc_address': '123 Something St',
        'cc_city': 'Someplace',
        'cc_state': 'NY',
        'cc_zip': '12345',
        'plan_code': 'PAID_MONTHLY',
    }
    
    def get_product(self):
        product = CheddarProduct(**self.client_defaults)
        
        return product

    def test_instantiate_product(self):
        product = self.get_product()
        
        for key, value in self.client_defaults.items():
            self.assertEquals(value, getattr(product.client, key))
            
    def test_get_all_plans(self):
        product = self.get_product()
        
        plans = product.get_all_plans()
        
        for plan in plans:
            if plan.code == 'FREE_MONTHLY':
                free_plan = plan
            elif plan.code == 'PAID_MONTHLY':
                paid_plan = plan
            elif plan.code == 'TRACKED_MONTHLY':
                tracked_plan = plan
            
        self.assertEquals('FREE_MONTHLY', free_plan.code)
        self.assertEquals('PAID_MONTHLY', paid_plan.code)
        self.assertEquals('TRACKED_MONTHLY', tracked_plan.code)
        
    def test_get_plan(self):
        product = self.get_product()
        code = 'PAID_MONTHLY'
        plan = product.get_plan(code)
        
        self.assertEquals(code, plan.code)
        
    def test_plan_initial_bill_date(self):
        product = self.get_product()
        code = 'PAID_MONTHLY'
        plan = product.get_plan(code)
        
        expected = date.today() + relativedelta(months=1)
        result = plan.initial_bill_date
        
        self.assertEquals(expected, result)
        
    def get_customer(self, **kwargs):
        customer_data = copy(self.customer_defaults)
        customer_data.update(kwargs)
        product = self.get_product()
        
        customer = product.create_customer(**customer_data)
        
        return customer
        
    def get_customer_with_items(self, **kwargs):
        data = copy(self.paid_defaults)
        if 'items' in kwargs.keys():
            items = kwargs['items']
        else:
            items = []
            items.append({'code': 'MONTHLY_ITEM', 'quantity': 3})
            items.append({'code': 'ONCE_ITEM'})
        
        data['items'] = items
        data['plan_code'] = 'TRACKED_MONTHLY'
        customer = self.get_customer(**data)
        
        return customer
    
    @clear_users
    def test_simple_create_customer(self):
        self.get_customer()
        
    @clear_users
    def test_create_customer_with_company(self):
        self.get_customer(company='Test Co')
        
    @clear_users
    def test_create_customer_with_meta_data(self):
        self.get_customer(meta_data = {'key_1': 'value_1', 'key2': 'value_2'})
    
    @clear_users
    def test_create_customer_with_true_vat_excempt(self):
        self.get_customer(is_vat_excempt=True)
    
    @clear_users
    def test_create_customer_with_false_vat_excempt(self):
        self.get_customer(is_vat_excempt=False)
        
    @clear_users
    def test_create_customer_with_vat_number(self):
        self.get_customer(vat_number=12345)
        
    @clear_users
    def test_create_customer_with_notes(self):
        self.get_customer(notes='This is a test note!')
        
    @clear_users
    def test_create_customer_with_first_contact_datetime(self):
        self.get_customer(first_contact_datetime=datetime.now())
        
    @clear_users
    def test_create_customer_with_referer(self):
        self.get_customer(referer='http://saaspire.com/test.html')
        
    @clear_users
    def test_create_customer_with_campaign_term(self):
        self.get_customer(campaign_term='testing')
        
    @clear_users
    def test_create_customer_with_campaign_name(self):
        self.get_customer(campaign_name='testing')
        
    @clear_users
    def test_create_customer_with_campaign_source(self):
        self.get_customer(campaign_source='testing')
        
    @clear_users
    def test_create_customer_with_campaign_content(self):
        self.get_customer(campaign_content='testing')
        
    @clear_users
    def test_create_customer_with_initial_bill_date(self):
        initial_bill_date = datetime.utcnow() + timedelta(days=60)
        customer = self.get_customer(initial_bill_date=initial_bill_date)
        invoice = customer.subscription.invoices[0]
        real_bill_date = invoice['billing_datetime']
        
        # Sometimes cheddar getter will push the bill date to the next day 
        # if the request is made around UTC midnight
        diff = initial_bill_date.date() - real_bill_date.date()
        self.assertLessEqual(diff.days, 1)
        
    @clear_users
    def test_create_paid_customer(self):
        self.get_customer(**self.paid_defaults)
        
    @clear_users
    def test_create_paid_customer_with_charges(self):
        data = copy(self.paid_defaults)
        charges = []
        charges.append({'code': 'test_charge_1', 'each_amount': Decimal('2.30')})
        charges.append({'code': 'charge2', 'amount': 3, 'each_amount': 4})
        data['charges'] = charges
        self.get_customer(**data)
        
        
    @clear_users
    def test_create_paid_customer_with_items(self):
        data = copy(self.paid_defaults)
        items = []
        items.append({'code': 'MONTHLY_ITEM', 'quantity': 3})
        items.append({'code': 'ONCE_ITEM'})
        data['items'] = items
        data['plan_code'] = 'TRACKED_MONTHLY'
        self.get_customer(**data)
        
    @clear_users
    def test_customer_repr(self):
        customer = self.get_customer()

        expected = 'Customer: Test User (test)'
        result = repr(customer)

        self.assertEquals(expected, result)
        
    @clear_users
    def test_subscription_repr(self):
        customer = self.get_customer()
        subscription = customer.subscription
        
        expected = 'Subscription:'
        result = repr(subscription)
        
        self.assertIn(expected, result)
        
    @clear_users
    def test_pricing_plan_repr(self):
        customer = self.get_customer()
        subscription = customer.subscription
        plan = subscription.plan
        
        expected = 'PricingPlan: Free Monthly (FREE_MONTHLY)'
        result = repr(plan)
        
        self.assertEquals(expected, result)
        
        
    @clear_users
    def test_item_repr(self):
        customer = self.get_customer_with_items()
        subscription = customer.subscription
        item = subscription.items['MONTHLY_ITEM']
        
        expected = 'Item: MONTHLY_ITEM for test'
        result = repr(item)
        
        self.assertEquals(expected, result)
        
    @clear_users
    def test_get_customers(self):
        customer1 = self.get_customer()
        customer2_data = copy(self.paid_defaults)
        customer2_data.update({
            'code': 'test2',
            'email':'garbage+2@saaspire.com',
            'first_name': 'Test2',
            'last_name': 'User2',
        })
        customer2 = self.get_customer(**customer2_data)
        product = self.get_product()
        
        fetched_customers = product.get_customers()
        
        self.assertEquals(2, len(fetched_customers))
        
    @clear_users
    def test_get_customer(self):
        created_customer = self.get_customer()
        product = self.get_product()
        
        fetched_customer = product.get_customer(code=created_customer.code)
        
        self.assertEquals(created_customer.code, fetched_customer.code)
        self.assertEquals(created_customer.first_name, fetched_customer.first_name)
        self.assertEquals(created_customer.last_name, fetched_customer.last_name)
        self.assertEquals(created_customer.email, fetched_customer.email)
        
    @clear_users
    def test_simple_customer_update(self):
        new_name = 'Different'
        customer = self.get_customer()
        product = self.get_product()
        
        customer.update(first_name=new_name)
        self.assertEquals(new_name, customer.first_name)
        
        fetched_customer = product.get_customer(code=customer.code)
        self.assertEquals(customer.first_name, fetched_customer.first_name)
        
    @clear_users
    @raises(NotFound)
    def test_delete_customer(self):
        customer = self.get_customer()
        product = self.get_product()
        
        fetched_customer = product.get_customer(code=customer.code)
        self.assertEquals(customer.first_name, fetched_customer.first_name)
        
        customer.delete()
        fetched_customer = product.get_customer(code=customer.code)
        
        
    @clear_users
    def test_delete_all_customers(self):
        customer_1 = self.get_customer()
        customer_2 = self.get_customer(code='test2')
        product = self.get_product()
        
        fetched_customers = product.get_customers()
        self.assertEquals(2, len(fetched_customers))
        
        product.delete_all_customers()
        
        fetched_customers = product.get_customers()
        self.assertEquals(0, len(fetched_customers))
        
    @clear_users
    def test_cancel_subscription(self):
        customer = self.get_customer()
        customer.subscription.cancel()
        
        now = datetime.now(tzutc())
        canceled_on = customer.subscription.canceled
        diff = now - canceled_on
        limit = timedelta(seconds=10)
        
        self.assertLess(diff, limit)
        
    def assert_increment(self, quantity=None):
        customer = self.get_customer_with_items()
        product = self.get_product()
        item = customer.subscription.items['MONTHLY_ITEM']
        
        old_quantity = item.quantity_used
        item.increment(quantity)
        new_quantity = item.quantity_used
        diff = new_quantity - old_quantity
        expected = Decimal(quantity or 1)
        self.assertAlmostEqual(expected, diff, places=2)
        
        fetched_customer = product.get_customer(code=customer.code)
        fetched_item = customer.subscription.items[item.code]
        self.assertEquals(item.quantity_used, fetched_item.quantity_used)
        
    @clear_users
    def test_simple_increment(self):
        self.assert_increment()
        
    @clear_users
    def test_int_increment(self):
        self.assert_increment(1)
        
    @clear_users
    def test_float_increment(self):
        self.assert_increment(1.234)
    
    @clear_users
    def test_decimal_increment(self):
        self.assert_increment(Decimal('1.234'))
        
    def assert_decrement(self, quantity=None):
        customer = self.get_customer_with_items()
        product = self.get_product()
        item = customer.subscription.items['MONTHLY_ITEM']
        
        old_quantity = item.quantity_used
        item.decrement(quantity)
        new_quantity = item.quantity_used
        diff = old_quantity - new_quantity
        expected = Decimal(quantity or 1)
        self.assertAlmostEqual(expected, diff, places=2)
        
        fetched_customer = product.get_customer(code=customer.code)
        fetched_item = customer.subscription.items[item.code]
        self.assertEquals(item.quantity_used, fetched_item.quantity_used)
        
    @clear_users
    def test_simple_decrement(self):
        self.assert_decrement()
        
    @clear_users
    def test_int_decrement(self):
        self.assert_decrement(1)
        
    @clear_users
    def test_float_decrement(self):
        self.assert_decrement(1.234)
    
    @clear_users
    def test_decimal_decrement(self):
        self.assert_decrement(Decimal('1.234'))
        
    def assert_set(self, quantity):
        customer = self.get_customer_with_items()
        product = self.get_product()
        item = customer.subscription.items['MONTHLY_ITEM']
        
        old_quantity = item.quantity_used
        item.set(quantity)
        new_quantity = item.quantity_used
        expected = Decimal(quantity)
        self.assertAlmostEqual(expected, new_quantity, places=2)
        
        fetched_customer = product.get_customer(code=customer.code)
        fetched_item = customer.subscription.items[item.code]
        self.assertEquals(item.quantity_used, fetched_item.quantity_used)
        
    @clear_users
    def test_int_set(self):
        self.assert_set(1)
        
    @clear_users
    def test_float_set(self):
        self.assert_set(1.234)
    
    @clear_users
    def test_decimal_set(self):
        self.assert_set(Decimal('1.234'))
        
    def assert_charged(self, code, each_amount, quantity=None,
                        description=None):
        customer = self.get_customer(**self.paid_defaults)
        product = self.get_product()
    
        customer.charge(
            code=code,
            each_amount=each_amount,
            quantity=quantity,
            description=description,
        )
        
        if description is None:
            description = ''
        
        found_charge = None
        for invoice in customer.subscription.invoices:
            for charge in invoice['charges']:
                if charge['code'] == code:
                    found_charge = charge
        
        self.assertAlmostEqual(Decimal(each_amount), found_charge['each_amount'], places=2)
        self.assertEqual(quantity, found_charge['quantity'])
        self.assertEqual(description, found_charge['description'])
        
        fetched_customer = product.get_customer(code=customer.code)
        fetched_charge = None
        for invoice in fetched_customer.subscription.invoices:
            for charge in invoice['charges']:
                if charge['code'] == code:
                    fetched_charge = charge
        
        self.assertAlmostEqual(Decimal(each_amount), fetched_charge['each_amount'], places=2)
        self.assertEqual(quantity, fetched_charge['quantity'])
        self.assertEqual(description, fetched_charge['description'])
    
    @clear_users
    def test_add_charge(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=1, quantity=1)
        
    @clear_users
    def test_add_float_charge(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=2.3, quantity=2)
        
    @clear_users
    def test_add_float_charge(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=2.3, quantity=2)
        
    @clear_users
    def test_add_decimal_charge(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=Decimal('2.3'), quantity=3)
        
    @clear_users
    def test_add_charge_with_descriptions(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=1, quantity=1, description="A test charge")
        
    @clear_users
    def test_add_credit(self):
        self.assert_charged(code='TEST-CHARGE', each_amount=-1, quantity=1)