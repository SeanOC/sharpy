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
        
    def create_customer(self, code, first_name, last_name, email, plan_code, \
                        company=None, is_vat_excempt=None, vat_number=None, \
                        notes=None, first_contact_datetime=None, \
                        referer=None, campaign_term=None, \
                        campaign_name=None, campaign_source=None, \
                        campaign_medium=None, campaign_content=None, \
                        meta_data=None, initial_bill_date=None, \
                        cc_number=None, cc_expiration=None, \
                        cc_card_code=None, cc_first_name=None, \
                        cc_last_name=None, cc_company=None, \
                        cc_country=None, cc_address=None, cc_city=None, \
                        cc_state=None, cc_zip=None, charges=None, items=None):
                        
        # Required data
        data = {
            'code': code,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'subscription[planCode]': plan_code,
        }
        
        # Optional data
        if company:
            data['company'] = company
            
        if is_vat_excempt is not None:
            if is_vat_excempt:
                data['isVatExcempt'] = 1
            else:
                data['isVatExcempt'] = 0
        
        if vat_number:
            data['vatNumber'] = vat_number
        
        if notes:
            data['notes'] = notes
            
        if first_contact_datetime:
            data['firstContactDatetime'] = self.client.format_datetime(first_contact_datetime)
        
        if referer:
            data['referer'] = referer
        
        if campaign_term:
            data['campaignTerm'] = campaign_term
            
        if campaign_name:
            data['campaignName'] = campaign_name
        
        if campaign_source:
            data['campaignSource'] = campaign_source
        
        if campaign_content:
            data['campaignContent'] = campaign_content
        
        if meta_data:
            for key, value in meta_data.iteritems():
                full_key = 'metaData[%s]' % key
                data[full_key] = value
        
        if initial_bill_date:
            data['subscription[initialBillDate]'] = self.client.format_datetime(initial_bill_date)
        
        if cc_number:
            data['subscription[ccNumber]'] = cc_number
        
        if cc_expiration:
            data['subscription[ccExpiration]'] = cc_expiration.strftime('%m/%Y')
        
        if cc_card_code:
            data['subscription[ccCardCode]']
        
        if cc_first_name:
            data['subscription[ccFirstName]'] = cc_first_name
        
        if cc_last_name:
            data['subscription[ccLastName]'] = cc_last_name
        
        if cc_company:
            data['subscription[ccCompany]'] = cc_company
        
        if cc_country:
            data['subscription[ccCountry]'] = cc_country
        
        if cc_address:
            data['subscription[ccAddress]'] = cc_addresss
        
        if cc_city:
            data['subscription[ccCity]'] = cc_city
        
        if cc_state:
            data['subscription[ccState]'] = cc_state
        
        if cc_zip:
            data['subscription[ccZip]'] = cc_zip
        
        if charges:
            for i, charge in enumerate(charges):
                data['charges[%d][chargeCode]' % i] = charge['code']
                data['charges[%d][quantity]' % i] = charge.get('quantity', 1)
                data['charges[%d][eachAmount]' % i] = charge['each_amount']
                data['charges[%d][description]' % i] = charge.get('description', '')
        
        if items:
            for i, item in enumerate(items):
                data['items[%d][itemCode]' % i] = item['code']
                data['items[%d][quantity]' % i] = item.get('quantity', 0)
        
        response = self.client.make_request(path='customers/new', data=data)
        print response.content
        
                                
                            
        
    def get_customers(self):
        response = self.client.make_request(path='customers/get')
        print response.content
        
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