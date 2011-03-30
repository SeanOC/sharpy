from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import logging

from dateutil import parser as date_parser

try:
    from lxml.etree import XML
except ImportError:
    from elementtree.ElementTree import XML
    
from sharpy.exceptions import ParseError

client_log = logging.getLogger('SharpyClient')

def parse_error(xml_str):
    error = {}
    doc = XML(xml_str)
    if doc.tag == 'error':
        elem = doc
    elif doc.tag == 'customers':
        elem = doc.find('.//error')
    else:
        raise Exception("Can't find error element in '%s'" % xml_str)
    client_log.debug(elem)
    error['id'] = elem.attrib['id']
    error['code'] = elem.attrib['code']
    error['aux_code'] = elem.attrib['auxCode']
    error['message'] = elem.text
    
    return error
    

class CheddarOutputParser(object):
    '''
    A utility class for parsing the various datatypes returned by the
    cheddar api.
    '''
    def parse_bool(self, content):
        if content == '' and content is not None:
            value = None
        elif content == '1':
            value = True
        elif content == '0':
            value = False
        else:
            raise ParseError("Can't parse '%s' as a bool." % content)
        
        return value
        
    def parse_int(self, content):
        value = None
        if content != '' and content is not None:
            try:
                value = int(content)
            except ValueError:
                raise ParseError("Can't parse '%s' as an int." % content)
            
        return value
        
    def parse_decimal(self, content):
        value = None
        if content != '' and content is not None:
            try:
                value = Decimal(content)
            except InvalidOperation:
                raise ParseError("Can't parse '%s' as a decimal." % content)
            
        return value
        
    def parse_datetime(self, content):
        value = None
        if content:
            try:
                value = date_parser.parse(content)
            except ValueError:
                raise ParseError("Can't parse '%s' as a datetime." % content)
            
            
        return value
        
class PlansParser(CheddarOutputParser):
    '''
    A utility class for parsing cheddar's xml output for pricing plans.
    '''
    def parse_xml(self, xml_str):
        plans = []
        plans_xml = XML(xml_str)
        for plan_xml in plans_xml:
            plan = self.parse_plan(plan_xml)
            plans.append(plan)
        
        return plans
        
    def parse_plan(self, plan_element):
        plan = {}
        plan['id'] = plan_element.attrib['id']
        plan['code'] = plan_element.attrib['code']
        plan['name'] = plan_element.findtext('name')
        plan['description'] = plan_element.findtext('description')
        plan['is_active'] = self.parse_bool(plan_element.findtext('isActive'))
        plan['is_free'] = self.parse_bool(plan_element.findtext('isFree'))
        plan['trial_days'] = self.parse_int(plan_element.findtext('trialDays'))
        plan['initial_bill_count'] = self.parse_int(plan_element.findtext('initialBillCount'))
        plan['initial_bill_count_unit'] = plan_element.findtext('initialBillCountUnit')
        plan['billing_frequency'] = plan_element.findtext('billingFrequency')
        plan['billing_frequency_per'] = plan_element.findtext('billingFrequencyPer')
        plan['billing_frequency_unit'] = plan_element.findtext('billingFrequencyUnit')
        plan['billing_frequency_quantity'] = self.parse_int(plan_element.findtext('billingFrequencyQuantity'))
        plan['setup_charge_code'] = plan_element.findtext('setupChargeCode')
        plan['setup_charge_amount'] = self.parse_decimal(plan_element.findtext('setupChargeAmount'))
        plan['recurring_charge_code'] = plan_element.findtext('recurringChargeCode')
        plan['recurring_charge_amount'] = self.parse_decimal(plan_element.findtext('recurringChargeAmount'))
        plan['created_datetime'] = self.parse_datetime(plan_element.findtext('createdDatetime'))
        
        plan['items'] = self.parse_plan_items(plan_element.find('items'))
        
        return plan
        
    def parse_plan_items(self, items_element):
        items = []
        
        if items_element is not None:
            for item_element in items_element:
                items.append(self.parse_plan_item(item_element))
        
        return items
    
    def parse_plan_item(self, item_element):
        item = {}
        
        item['id'] = item_element.attrib['id']
        item['code'] = item_element.attrib['code']
        item['name'] = item_element.findtext('name')
        item['quantity_included'] = self.parse_decimal(item_element.findtext('quantityIncluded'))
        item['is_periodic'] = self.parse_bool(item_element.findtext('isPeriodic'))
        item['overage_amount'] = self.parse_decimal(item_element.findtext('overageAmount'))
        item['created_datetime'] = self.parse_datetime(item_element.findtext('createdDatetime'))
        
        return item
        
        
class CustomersParser(CheddarOutputParser):
    '''
    Utility class for parsing cheddar's xml output for customers.
    '''
    def parse_xml(self, xml_str):
        customers = []
        customers_xml = XML(xml_str)
        for customer_xml in customers_xml:
            customer = self.parse_customer(customer_xml)
            customers.append(customer)
            
        return customers
    
    def parse_customer(self, customer_element):
        customer = {}
        
        # Basic info
        customer['id'] = customer_element.attrib['id']
        customer['code'] = customer_element.attrib['code']
        customer['first_name'] = customer_element.findtext('firstName')
        customer['last_name'] = customer_element.findtext('lastName')
        customer['company'] = customer_element.findtext('company')
        customer['email'] = customer_element.findtext('email')
        customer['notes'] = customer_element.findtext('notes')
        customer['gateway_token'] = customer_element.findtext('gateway_token')
        customer['is_vat_excempt'] = customer_element.findtext('isVatExcempt')
        customer['vat_number'] = customer_element.findtext('vatNumber')
        customer['first_contact_datetime'] = self.parse_datetime(customer_element.findtext('firstContactDatetime'))
        customer['referer'] = customer_element.findtext('referer')
        customer['referer_host'] = customer_element.findtext('refererHost')
        customer['campaign_source'] = customer_element.findtext('campaignSource')
        customer['campaign_medium'] = customer_element.findtext('campaignMedium')
        customer['campaign_term'] = customer_element.findtext('campaignTerm')
        customer['campaign_content'] = customer_element.findtext('campaignContent')
        customer['campaign_name'] = customer_element.findtext('campaignName')
        customer['created_datetime'] = self.parse_datetime(customer_element.findtext('createdDatetime'))
        customer['modified_datetime'] = self.parse_datetime(customer_element.findtext('modifiedDatetime'))
        
        # Metadata
        customer['meta_data'] = self.parse_meta_data(customer_element.find('metaData'))
        
        # Subscriptions
        customer['subscriptions'] = self.parse_subscriptions(customer_element.find('subscriptions'))
        
        return customer
    
    def parse_meta_data(self, meta_data_element):
        meta_data = []
        for meta_datum_element in meta_data_element:
            meta_data.append(self.parse_meta_datum(meta_datum_element))
        
        return meta_data
    
    def parse_meta_datum(self, meta_datum_element):
        meta_datum = {}
        
        meta_datum['id'] = meta_datum_element.attrib['id']
        meta_datum['name'] = meta_datum_element.findtext('name')
        meta_datum['value'] = meta_datum_element.findtext('value')
        meta_datum['created_datetime'] = self.parse_datetime(meta_datum_element.findtext('createdDatetime'))
        meta_datum['modified_datetime'] = self.parse_datetime(meta_datum_element.findtext('modifiedDatetime'))
        
        return meta_datum
        
        
    def parse_subscriptions(self, subscriptions_element):
        subscriptions = []
        for subscription_element in subscriptions_element:
            subscription = self.parse_subscription(subscription_element)
            subscriptions.append(subscription)
            
        return subscriptions
        
    def parse_subscription(self, subscription_element):
        subscription = {}
        
        # Basic info
        subscription['id'] = subscription_element.attrib['id']
        subscription['gateway_token'] = subscription_element.findtext('gatewayToken')
        subscription['cc_first_name'] = subscription_element.findtext('ccFirstName')
        subscription['cc_last_name'] = subscription_element.findtext('ccLastName')
        subscription['cc_company'] = subscription_element.findtext('ccCompany')
        subscription['cc_country'] = subscription_element.findtext('ccCountry')
        subscription['cc_address'] = subscription_element.findtext('ccAddress')
        subscription['cc_city'] = subscription_element.findtext('ccCity')
        subscription['cc_state'] = subscription_element.findtext('ccState')
        subscription['cc_zip'] = subscription_element.findtext('ccZip')
        subscription['cc_type'] = subscription_element.findtext('ccType')
        subscription['cc_last_four'] = subscription_element.findtext('ccLastFour')
        subscription['cc_expiration_date'] = subscription_element.findtext('ccExpirationDate')
        subscription['canceled_datetime'] = self.parse_datetime(subscription_element.findtext('canceledDatetime'))
        subscription['created_datetime'] = self.parse_datetime(subscription_element.findtext('createdDatetime'))
        
        # Plans
        subscription['plans'] = self.parse_plans(subscription_element.find('plans'))
        
        # Invoices
        subscription['invoices'] = self.parse_invoices(subscription_element.find('invoices'))
        
        subscription['items'] = self.parse_subscription_items(subscription_element.find('items'))
        
        return subscription
        
    def parse_plans(self, plans_element):
        plans_parser = PlansParser()
        plans = []
        
        if plans_element is not None:
            for plan_element in plans_element:
                plans.append(plans_parser.parse_plan(plan_element))
            
        return plans
        
    def parse_invoices(self, invoices_element):
        invoices = []
        
        for invoice_element in invoices_element:
            invoices.append(self.parse_invoice(invoice_element))
            
        return invoices
    
    def parse_invoice(self, invoice_element):
        invoice = {}
        
        invoice['id'] = invoice_element.attrib['id']
        invoice['number'] = invoice_element.findtext('number')
        invoice['type'] = invoice_element.findtext('type')
        invoice['vat_rate'] = invoice_element.findtext('vatRate')
        invoice['billing_datetime'] = self.parse_datetime(invoice_element.findtext('billingDatetime'))
        invoice['paid_transaction_id'] = invoice_element.findtext('paidTransactionId')
        invoice['created_datetime'] = self.parse_datetime(invoice_element.findtext('createdDatetime'))
        
        invoice['charges'] = self.parse_charges(invoice_element.find('charges'))
        
        return invoice
        
    def parse_charges(self, charges_element):
        charges = []
        
        for charge_element in charges_element:
            charges.append(self.parse_charge(charge_element))
        
        return charges
        
    def parse_charge(self, charge_element):
        charge = {}
        
        charge['id'] = charge_element.attrib['id']
        charge['code'] = charge_element.attrib['code']
        charge['type'] = charge_element.findtext('type')
        charge['quantity'] = self.parse_decimal(charge_element.findtext('quantity'))
        charge['each_amount'] = self.parse_decimal(charge_element.findtext('eachAmount'))
        charge['description'] = charge_element.findtext('description')
        charge['created_datetime'] = self.parse_datetime(charge_element.findtext('createdDatetime'))
        
        return charge
        
    def parse_subscription_items(self, items_element):
        items = []
        
        if items_element is not None:
            for item_element in items_element:
                items.append(self.parse_subscription_item(item_element))
            
        return items
        
    def parse_subscription_item(self, item_element):
        item = {}

        item['id'] = item_element.attrib['id']
        item['code'] = item_element.attrib['code']
        item['name'] = item_element.findtext('name')
        item['quantity'] = self.parse_decimal(item_element.findtext('quantity'))
        item['created_datetime'] = self.parse_datetime(item_element.findtext('createdDatetime'))
        item['modified_datetime'] = self.parse_datetime(item_element.findtext('modifiedDatetime'))
        
        return item
        