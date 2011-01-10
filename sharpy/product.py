from sharpy.client import Client
from sharpy.parsers import PlansParser

class CheddarProduct(object):
    
    def __init__(self, username, password, product_code, cache=None, timeout=None, endpoint=None):
        self.product_code = product_code
        self.client = Client(
            username,
            password,
            product_code,
            cache,
            timeout,
            endpoint,
        )
        
        super(CheddarProduct, self).__init__()
        
    def __repr__(self):
        return u'CheddarProduct: %s' % self.product_code
        
    def get_all_plans(self):
        response = self.client.make_request(path='plans/get')
        plans_parser = PlansParser()
        plans_data = plans_parser.parse_xml(response.content)
        plans = [PricingPlan(**plan_data) for plan_data in plans_data]
        
        return plans
        
    def get_plan(self, code):
        response = self.client.make_request(
            path='plans/get',
            params={'code': code},
        )
        plans_parser = PlansParser()
        plans_data = plans_parser.parse_xml(response.content)
        plans = [PricingPlan(**plan_data) for plan_data in plans_data]
        
        return plans[0]
        
class PricingPlan(object):
    
    def __init__(self, name, code, id, description, is_active, is_free, \
                 trial_days, billing_frequency, billing_frequency_per, \
                 billing_frequency_quantity, billing_frequency_unit,  \
                 setup_charge_code, setup_charge_amount, \
                 recurring_charge_code, recurring_charge_amount, \
                 created_datetime):
        self.name = name
        self.code = code
        self.id = id
        self.description = description
        self.is_active = is_active
        self.is_free = is_free
        self.trial_days = trial_days
        self.billing_frequency = billing_frequency
        self.billing_frequency_per = billing_frequency_per
        self.billing_frequency_quantity = billing_frequency_quantity
        self.billing_frequency_unit = billing_frequency_unit
        self.setup_charge_code = setup_charge_code
        self.setup_charge_amount = setup_charge_amount
        self.recurring_charge_code = recurring_charge_code
        self.recurring_charge_amount = recurring_charge_amount
        self.created_datetime = created_datetime
        
    def __repr__(self):
        return u'PricingPlan: %s (%s)' % (self.name, self.code)