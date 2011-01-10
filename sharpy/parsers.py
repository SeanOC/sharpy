from datetime import datetime
from decimal import Decimal, InvalidOperation

from dateutil import parser as date_parser

try:
    from lxml.etree import XML
except ImportError:
    from elementtree.ElementTree import XML
    
from sharpy.exceptions import ParseError

def parse_error(xml_str):
    error = {}
    elem = XML(xml_str)
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
        if content == '1':
            value = True
        elif content == '0':
            value = False
        else:
            raise ParseError("Can't parse '%s' as a bool." % content)
        
        return value
        
    def parse_int(self, content):
        try:
            value = int(content)
        except ValueError:
            raise ParseError("Can't parse '%s' as an int." % content)
            
        return value
        
    def parse_decimal(self, content):
        try:
            value = Decimal(content)
        except InvalidOperation:
            raise ParseError("Can't parse '%s' as a decimal." % content)
            
        return value
        
    def parse_datetime(self, content):
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
            plan = {}
            plan['id'] = plan_xml.attrib['id']
            plan['code'] = plan_xml.attrib['code']
            plan['name'] = plan_xml.findtext('name')
            plan['description'] = plan_xml.findtext('description')
            plan['is_active'] = self.parse_bool(plan_xml.findtext('isActive'))
            plan['is_free'] = self.parse_bool(plan_xml.findtext('isFree'))
            plan['trial_days'] = self.parse_int(plan_xml.findtext('trialDays'))
            plan['billing_frequency'] = plan_xml.findtext('billingFrequency')
            plan['billing_frequency_per'] = plan_xml.findtext('billingFrequencyPer')
            plan['billing_frequency_unit'] = plan_xml.findtext('billingFrequencyUnit')
            plan['billing_frequency_quantity'] = self.parse_int(plan_xml.findtext('billingFrequencyQuantity'))
            plan['setup_charge_code'] = plan_xml.findtext('setupChargeCode')
            plan['setup_charge_amount'] = self.parse_decimal(plan_xml.findtext('setupChargeAmount'))
            plan['recurring_charge_code'] = plan_xml.findtext('recurringChargeCode')
            plan['recurring_charge_amount'] = self.parse_decimal(plan_xml.findtext('recurringChargeAmount'))
            plan['created_datetime'] = self.parse_datetime(plan_xml.findtext('createdDatetime'))
            
            plans.append(plan)
        
        return plans