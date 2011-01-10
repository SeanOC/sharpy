from copy import copy
from datetime import datetime, timedelta
from decimal import Decimal
import unittest

from testconfig import config

from sharpy.product import CheddarProduct

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
        
    def get_customer(self, **kwargs):
        customer_data = copy(self.customer_defaults)
        customer_data.update(kwargs)
        product = self.get_product()
        
        customer = product.create_customer(**customer_data)
        
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
        initial_bill_date = datetime.now() + timedelta(days=30)
        self.get_customer(initial_bill_date=initial_bill_date)
        
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