from copy import copy
from datetime import date
from decimal import Decimal, getcontext as get_decimal_context

from dateutil.relativedelta import relativedelta

from sharpy.client import Client
from sharpy.exceptions import NotFound
from sharpy.parsers import PlansParser, CustomersParser

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
                        
        data = self.build_customer_post_data(code, first_name, last_name, \
                    email, plan_code, company, is_vat_excempt, vat_number, \
                    notes, first_contact_datetime, referer, campaign_term, \
                    campaign_name, campaign_source, campaign_medium, \
                    campaign_content, meta_data, initial_bill_date, \
                    cc_number, cc_expiration, cc_card_code, cc_first_name, \
                    cc_last_name, cc_company, cc_country, cc_address, \
                    cc_city, cc_state, cc_zip)
        
        if charges:
            for i, charge in enumerate(charges):
                data['charges[%d][chargeCode]' % i] = charge['code']
                data['charges[%d][quantity]' % i] = charge.get('quantity', 1)
                data['charges[%d][eachAmount]' % i] = charge['each_amount']
                data['charges[%d][description]' % i] = charge.get('description', '')

        if items:
            for i, item in enumerate(items):
                data['items[%d][itemCode]' % i] = item['code']
                data['items[%d][quantity]' % i] = item.get('quantity', 1)
        
        response = self.client.make_request(path='customers/new', data=data)
        cusotmer_parser = CustomersParser()
        customers_data = cusotmer_parser.parse_xml(response.content)
        customer = Customer(product=self, **customers_data[0])
        
        return customer
        
    def build_customer_post_data(self, code=None, first_name=None,\
                last_name=None, email=None, plan_code=None, \
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
                cc_state=None, cc_zip=None, bill_date=None):
        
        data = {}
        
        if code:
            data['code'] = code
        
        if first_name:
            data['firstName'] = first_name
        
        if last_name:
            data['lastName'] = last_name
            
        if email:
            data['email'] = email
        
        if plan_code:
            data['subscription[planCode]'] = plan_code
        
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
            data['subscription[initialBillDate]'] = self.client.format_date(initial_bill_date)

        if cc_number:
            data['subscription[ccNumber]'] = cc_number

        if cc_expiration:
            data['subscription[ccExpiration]'] = cc_expiration

        if cc_card_code:
            data['subscription[ccCardCode]'] = cc_card_code

        if cc_first_name:
            data['subscription[ccFirstName]'] = cc_first_name

        if cc_last_name:
            data['subscription[ccLastName]'] = cc_last_name

        if cc_company:
            data['subscription[ccCompany]'] = cc_company

        if cc_country:
            data['subscription[ccCountry]'] = cc_country

        if cc_address:
            data['subscription[ccAddress]'] = cc_address

        if cc_city:
            data['subscription[ccCity]'] = cc_city

        if cc_state:
            data['subscription[ccState]'] = cc_state

        if cc_zip:
            data['subscription[ccZip]'] = cc_zip
            
        
        if bill_date:
            data['subscription[changeBillDate]'] = self.client.format_datetime(bill_date)

        return data
        
    def get_customers(self):
        customers = []
        
        try:
            response = self.client.make_request(path='customers/get')
        except NotFound:
            response = None
        
        if response:
            cusotmer_parser = CustomersParser()
            customers_data = cusotmer_parser.parse_xml(response.content)
            for customer_data in customers_data:
                customers.append(Customer(product=self, **customer_data))
            
        return customers
        
    def get_customer(self, code):
        
        response = self.client.make_request(
            path='customers/get',
            params={'code': code},
        )
        cusotmer_parser = CustomersParser()
        customers_data = cusotmer_parser.parse_xml(response.content)
        
        return Customer(product=self, **customers_data[0])
    
    def delete_all_customers(self):
        '''
        This method does exactly what you think it does.  Calling this method
        deletes all customer data in your cheddar product and the configured
        gateway.  This action cannot be undone.
        
        DO NOT RUN THIS UNLESS YOU REALLY, REALLY, REALLY MEAN TO!
        '''
        response = self.client.make_request(
            path='customers/delete-all/confirm/1',
            method='POST'
        )
        
        
class PricingPlan(object):
    
    def __init__(self, name, code, id, description, is_active, is_free,
                 trial_days, initial_bill_count, initial_bill_count_unit, 
                 billing_frequency, billing_frequency_per,
                 billing_frequency_quantity, billing_frequency_unit,
                 setup_charge_code, setup_charge_amount,
                 recurring_charge_code, recurring_charge_amount,
                 created_datetime, items, subscription=None):
        
        self.load_data(name=name, code=code, id=id, description=description,
                        is_active=is_active, is_free=is_free,
                        trial_days=trial_days,
                        initial_bill_count=initial_bill_count,
                        initial_bill_count_unit=initial_bill_count_unit,
                        billing_frequency=billing_frequency,
                        billing_frequency_per=billing_frequency_per,
                        billing_frequency_quantity=billing_frequency_quantity,
                        billing_frequency_unit=billing_frequency_unit,
                        setup_charge_code=setup_charge_code,
                        setup_charge_amount=setup_charge_amount,
                        recurring_charge_code=recurring_charge_code,
                        recurring_charge_amount=recurring_charge_amount,
                        created_datetime=created_datetime, items=items,
                        subscription=subscription)
        
        super(PricingPlan, self).__init__()
        
    def load_data(self, name, code, id, description, is_active, is_free,
                 trial_days, initial_bill_count, initial_bill_count_unit, 
                 billing_frequency, billing_frequency_per,
                 billing_frequency_quantity, billing_frequency_unit,
                 setup_charge_code, setup_charge_amount,
                 recurring_charge_code, recurring_charge_amount,
                 created_datetime, items, subscription=None):
                 
        self.name = name
        self.code = code
        self.id = id
        self.description = description
        self.is_active = is_active
        self.is_free = is_free
        self.trial_days = trial_days
        self.initial_bill_count = initial_bill_count
        self.initial_bill_count_unit = initial_bill_count_unit
        self.billing_frequency = billing_frequency
        self.billing_frequency_per = billing_frequency_per
        self.billing_frequency_quantity = billing_frequency_quantity
        self.billing_frequency_unit = billing_frequency_unit
        self.setup_charge_code = setup_charge_code
        self.setup_charge_amount = setup_charge_amount
        self.recurring_charge_code = recurring_charge_code
        self.recurring_charge_amount = recurring_charge_amount
        self.created = created_datetime
        self.items = items

        if subscription:
            self.subscription = subscription
        
    def __repr__(self):
        return u'PricingPlan: %s (%s)' % (self.name, self.code)
        
    @property
    def initial_bill_date(self):
        '''
        An estimated initial bill date for an account created today,
        based on available plan info.
        '''
        time_to_start = None
        
        if self.initial_bill_count_unit == 'months':
            time_to_start = relativedelta(months=self.initial_bill_count)
        else:
            time_to_start = relativedelta(days=self.initial_bill_count)
        
        initial_bill_date = date.today() + time_to_start
        
        return initial_bill_date
        
        

class Customer(object):
    
    def __init__(self, code, first_name, last_name, email, product, id=None, \
                 company=None, notes=None, gateway_token=None, \
                 is_vat_excempt=None, vat_number=None, \
                 first_contact_datetime=None, referer=None, \
                 referer_host=None, campaign_source=None, \
                 campaign_medium=None, campaign_term=None, \
                 campaign_content=None, campaign_name=None, \
                 created_datetime=None, modified_datetime=None, \
                 meta_data=None, subscriptions=None):
                 
        self.load_data(code=code,
                       first_name=first_name, last_name=last_name,
                       email=email, product=product, id=id,
                       company=company, notes=notes,
                       gateway_token=gateway_token,
                       is_vat_excempt=is_vat_excempt,
                       vat_number=vat_number,
                       first_contact_datetime=first_contact_datetime,
                       referer=referer, referer_host=referer_host,
                       campaign_source=campaign_source,
                       campaign_medium=campaign_medium,
                       campaign_term=campaign_term,
                       campaign_content=campaign_content,
                       campaign_name=campaign_name,
                       created_datetime=created_datetime,
                       modified_datetime=modified_datetime,
                       meta_data=meta_data,
                       subscriptions=subscriptions
                      )
        
        super(Customer, self).__init__()
        
    def load_data(self, code, first_name, last_name, email, product, id=None,\
                  company=None, notes=None, gateway_token=None, \
                  is_vat_excempt=None, vat_number=None, \
                  first_contact_datetime=None, referer=None, \
                  referer_host=None, campaign_source=None, \
                  campaign_medium=None, campaign_term=None, \
                  campaign_content=None, campaign_name=None, \
                  created_datetime=None, modified_datetime=None, \
                  meta_data=None, subscriptions=None):
        self.code = code
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.product = product
        self.company = company
        self.notes = notes
        self.gateway_token = gateway_token
        self.is_vat_excempt = is_vat_excempt
        self.vat_number = vat_number
        self.first_contact_datetime = first_contact_datetime
        self.referer = referer
        self.referer_host = referer_host
        self.campaign_source = campaign_source
        self.campaign_medium = campaign_medium
        self.campaign_content = campaign_content
        self.campaign_name = campaign_name
        self.created = created_datetime
        self.modified = modified_datetime

        self.meta_data = {}
        if meta_data:
          for datum in meta_data:
              self.meta_data[datum['name']] = datum['value']
        subscription_data = subscriptions[0]
        subscription_data['customer'] = self
        if hasattr(self, 'subscription'):
            self.subscription.load_data(**subscription_data)
        else:
            self.subscription = Subscription(**subscription_data)
        
    def load_data_from_xml(self, xml):
        cusotmer_parser = CustomersParser()
        customers_data = cusotmer_parser.parse_xml(xml)
        customer_data = customers_data[0]
        self.load_data(product=self.product, **customer_data)
        
    def update(self, first_name=None, last_name=None, email=None, \
                company=None, is_vat_excempt=None, vat_number=None, \
                notes=None, first_contact_datetime=None, \
                referer=None, campaign_term=None, \
                campaign_name=None, campaign_source=None, \
                campaign_medium=None, campaign_content=None, \
                meta_data=None,
                cc_number=None, cc_expiration=None, \
                cc_card_code=None, cc_first_name=None, \
                cc_last_name=None, cc_company=None, \
                cc_country=None, cc_address=None, cc_city=None, \
                cc_state=None, cc_zip=None, plan_code=None, bill_date=None ):
        
        data = self.product.build_customer_post_data( first_name=first_name,
                        last_name=last_name, email=email, plan_code=plan_code,
                        company=company, is_vat_excempt=is_vat_excempt,
                        vat_number=vat_number, notes=notes, referer=referer,
                        campaign_term=campaign_term,
                        campaign_name=campaign_name,
                        campaign_source=campaign_source,
                        campaign_medium=campaign_medium,
                        campaign_content=campaign_content,
                        meta_data=meta_data,
                        cc_number=cc_number, cc_expiration=cc_expiration,
                        cc_card_code=cc_card_code,
                        cc_first_name=cc_first_name,
                        cc_last_name=cc_last_name, cc_company=cc_company,
                        cc_country=cc_country, cc_address=cc_address,
                        cc_city=cc_city, cc_state=cc_state, cc_zip=cc_zip)
        
        path = 'customers/edit'
        params = {'code': self.code}
        
        response = self.product.client.make_request(
            path = path,
            params = params,
            data = data,
        )
        return self.load_data_from_xml(response.content)
        
        
    def delete(self):
        path = 'customers/delete'
        params = {'code': self.code}
        response = self.product.client.make_request(
            path = path,
            params = params,
        )
        
    def charge(self, code, each_amount, quantity=1, description=None):
        '''
        Add an arbitrary charge or credit to a customer's account.  A positive
        number will create a charge.  A negative number will create a credit.
        
        each_amount is normalized to a Decimal with a precision of 2 as that
        is the level of precision which the cheddar API supports.
        '''
        each_amount = Decimal(each_amount)
        each_amount = each_amount.quantize(Decimal('.01'))
        data = {
            'chargeCode': code,
            'eachAmount': each_amount,
            'quantity': quantity,
        }
        if description:
            data['description'] = description
        
        response = self.product.client.make_request(
            path='customers/add-charge',
            params={'code': self.code},
            data=data,
        )
        return self.load_data_from_xml(response.content)
    
    def __repr__(self):
        return u'Customer: %s %s (%s)' % (
            self.first_name,
            self.last_name,
            self.code
        )
    
class Subscription(object):
    
    def __init__(self, id, gateway_token, cc_first_name, cc_last_name,
                 cc_company, cc_country, cc_address, cc_city, cc_state,
                 cc_zip, cc_type, cc_last_four, cc_expiration_date, customer,
                 canceled_datetime=None ,created_datetime=None,
                 plans=None, invoices=None, items=None):
        
        self.load_data(id=id, gateway_token=gateway_token, 
                        cc_first_name=cc_first_name,
                        cc_last_name=cc_last_name, 
                        cc_company=cc_company, cc_country=cc_country,
                        cc_address=cc_address, cc_city=cc_city,
                        cc_state=cc_state, cc_zip=cc_zip, cc_type=cc_type,
                        cc_last_four=cc_last_four,
                        cc_expiration_date=cc_expiration_date,
                        customer=customer,
                        canceled_datetime=canceled_datetime, 
                        created_datetime=created_datetime, plans=plans,
                        invoices=invoices, items=items)
        
        super(Subscription, self).__init__()
        
    def load_data(self, id, gateway_token, cc_first_name, cc_last_name, \
                 cc_company, cc_country, cc_address, cc_city, cc_state, \
                 cc_zip, cc_type, cc_last_four, cc_expiration_date, customer,\
                 canceled_datetime=None ,created_datetime=None, \
                 plans=None, invoices=None, items=None):
                 
        self.id = id
        self.gateway_token = gateway_token
        self.cc_first_name = cc_first_name
        self.cc_last_name = cc_last_name
        self.cc_company = cc_company
        self.cc_country = cc_country
        self.cc_address = cc_address
        self.cc_city = cc_city
        self.cc_state = cc_state
        self.cc_zip = cc_zip
        self.cc_type = cc_type
        self.cc_last_four = cc_last_four
        self.cc_expiration_date = cc_expiration_date
        self.canceled = canceled_datetime
        self.created = created_datetime
        self.invoices = invoices
        self.customer = customer

        # Organize item data into something more useful
        items_map = {}
        for item in items:
            items_map[item['code']] = {'subscription_data': item}
        plan_data = plans[0]
        for item in plan_data['items']:
            items_map[item['code']]['plan_data'] = item
        
        if not hasattr(self, 'items'):
            self.items = {}
        for code, item_map in items_map.iteritems():
            plan_item_data = item_map['plan_data']
            subscription_item_data = item_map['subscription_data']
            item_data = copy(plan_item_data)
            item_data.update(subscription_item_data)
            item_data['subscription'] = self
            
            if code in self.items.keys():
                item = self.items[code]
                item.load_data(**item_data)
            else:
                self.items[code] = Item(**item_data)

        plan_data['subscription'] = self
        if hasattr(self, 'plan'):
            self.plan.load_data(**plan_data)
        else:
            self.plan = PricingPlan(**plan_data)
    
    def __repr__(self):
        return u'Subscription: %s' % self.id
        
    def cancel(self):
        client = self.customer.product.client
        response = client.make_request(
            path='customers/cancel',
            params={'code': self.customer.code},
        )
        
        cusotmer_parser = CustomersParser()
        customers_data = cusotmer_parser.parse_xml(response.content)
        customer_data = customers_data[0]
        self.customer.load_data(
            product=self.customer.product,
            **customer_data
        )
        
class Item(object):
    
    def __init__(self, code, subscription, id=None, name=None,
                 quantity_included=None, is_periodic=None,
                 overage_amount=None, created_datetime=None,
                 modified_datetime=None, quantity=None):
                 
        self.load_data(code=code, subscription=subscription, id=id, name=name,
                      quantity_included=quantity_included,
                      is_periodic=is_periodic, overage_amount=overage_amount,
                      created_datetime=created_datetime,
                      modified_datetime=modified_datetime, quantity=quantity)
        
        super(Item, self).__init__()
        
    def load_data(self, code, subscription, id=None, name=None,
                 quantity_included=None, is_periodic=None,
                 overage_amount=None, created_datetime=None,
                 modified_datetime=None, quantity=None):
                 
        self.code = code
        self.subscription = subscription
        self.id = id
        self.name = name
        self.quantity_included = quantity_included
        self.quantity_used = quantity
        self.is_periodic = is_periodic
        self.overage_amount = overage_amount
        self.created = created_datetime
        self.modified = modified_datetime
    
    def __repr__(self):
        return u'Item: %s for %s' % (
            self.code,
            self.subscription.customer.code,
        )
        
    def _normalize_quantity(self, quantity=None):
        if quantity is not None:
            quantity = Decimal(quantity)
            quantity = quantity.quantize(Decimal('.0001'))
        
        return quantity
    
    def increment(self, quantity=None):
        '''
        Increment the item's quantity by the passed in amount.  If nothing is
        passed in, a quantity of 1 is assumed.  If a decimal value is passsed
        in, it is rounded to the 4th decimal place as that is the level of 
        precision which the Cheddar API accepts.
        '''
        data = {}
        if quantity:
            data['quantity'] = self._normalize_quantity(quantity)
        
        response = self.subscription.customer.product.client.make_request(
            path = 'customers/add-item-quantity',
            params = {
                'code': self.subscription.customer.code,
                'itemCode': self.code,
            },
            data = data,
            method = 'POST',
        )
        
        return self.subscription.customer.load_data_from_xml(response.content)
        
    def decrement(self, quantity=None):
        '''
        Decrement the item's quantity by the passed in amount.  If nothing is
        passed in, a quantity of 1 is assumed.  If a decimal value is passsed
        in, it is rounded to the 4th decimal place as that is the level of 
        precision which the Cheddar API accepts.
        '''
        data = {}
        if quantity:
            data['quantity'] = self._normalize_quantity(quantity)
         
        response = self.subscription.customer.product.client.make_request(
            path = 'customers/remove-item-quantity',
            params = {
                'code': self.subscription.customer.code,
                'itemCode': self.code,
            },
            data = data,
            method = 'POST',
        )
        
        return self.subscription.customer.load_data_from_xml(response.content)
        
    def set(self, quantity):
        '''
        Set the item's quantity to the passed in amount.  If nothing is
        passed in, a quantity of 1 is assumed.  If a decimal value is passsed
        in, it is rounded to the 4th decimal place as that is the level of 
        precision which the Cheddar API accepts.
        '''
        data = {}
        data['quantity'] = self._normalize_quantity(quantity)
         
        response = self.subscription.customer.product.client.make_request(
            path = 'customers/set-item-quantity',
            params = {
                'code': self.subscription.customer.code,
                'itemCode': self.code,
            },
            data = data,
            method = 'POST',
        )
        
        return self.subscription.customer.load_data_from_xml(response.content)
        
        