import unittest

from testconfig import config

from sharpy.product import CheddarProduct

class ProductTests(unittest.TestCase):
    
    client_defaults =  {
        'username': config['cheddar']['username'],
        'password': config['cheddar']['password'],
        'product_code': config['cheddar']['product_code'],
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
        print plans
        
        if plans[0].code == 'FREE_MONTHLY':
            free_plan = plans[0]
            paid_plan = plans[1]
        else:
            free_plan = plans[1]
            paid_plan = plans[0]
            
        self.assertEquals('FREE_MONTHLY', free_plan.code)
        self.assertEquals('PAID_MONTHLY', paid_plan.code)
        
    def test_get_plan(self):
        product = self.get_product()
        code = 'PAID_MONTHLY'
        plan = product.get_plan(code)
        
        self.assertEquals(code, plan.code)