from datetime import datetime
from decimal import Decimal
import os
import unittest

from dateutil.tz import tzutc
from nose.tools import raises

from sharpy.exceptions import ParseError
from sharpy.parsers import CheddarOutputParser, parse_error, PlansParser, CustomersParser

class ParserTests(unittest.TestCase):
    
    def load_file(self, filename):
        path = os.path.join(os.path.dirname(__file__), 'files', filename)
        f = open(path)
        content = f.read()
        f.close()
        return content
        
        
    def test_bool_parsing_true(self):
        parser = CheddarOutputParser()
        
        expected = True
        result = parser.parse_bool('1')
        
        self.assertEquals(expected, result)
        
    def test_bool_parsing_false(self):
        parser = CheddarOutputParser()
        
        expected = False
        result = parser.parse_bool('0')
        
        self.assertEquals(expected, result)
    
    @raises(ParseError)
    def test_bool_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_bool('test')
        
    def test_bool_parsing_empty(self):
        parser = CheddarOutputParser()

        expected = None
        result = parser.parse_bool('')

        self.assertEquals(expected, result)
        
    def test_int_parsing(self):
        parser = CheddarOutputParser()
        
        expected = 234
        result = parser.parse_int('234')
        
        self.assertEquals(expected, result)
        
    @raises(ParseError)
    def test_int_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_int('test')
        
    def test_int_parsing_empty(self):
        parser = CheddarOutputParser()

        expected = None
        result = parser.parse_int('')

        self.assertEquals(expected, result)
        
    def test_decimal_parsing(self):
        parser = CheddarOutputParser()
        
        expected = Decimal('2.345')
        result = parser.parse_decimal('2.345')
        
        self.assertEquals(expected, result)
    
    @raises(ParseError)
    def test_decimal_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_decimal('test')
        
    def test_decimal_parsing_empty(self):
        parser = CheddarOutputParser()

        expected = None
        result = parser.parse_decimal('')

        self.assertEquals(expected, result)
        
    def test_datetime_parsing(self):
        parser = CheddarOutputParser()
        
        expected = datetime(
            year=2011,
            month=1,
            day=7,
            hour=20,
            minute=46,
            second=43,
            tzinfo=tzutc(),
        )
        result = parser.parse_datetime('2011-01-07T20:46:43+00:00')
        
        self.assertEquals(expected, result)
    
    @raises(ParseError)
    def test_datetime_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_datetime('test')
        
    def test_datetime_parsing_empty(self):
        parser = CheddarOutputParser()
        
        expected = None
        result = parser.parse_datetime('')
        
        self.assertEquals(expected, result)
        
    
    def test_error_parser(self):
        error_xml = self.load_file('error.xml')
        
        expected = {
            'aux_code': '',
            'code': '400',
            'id': '149947',
            'message': 'No product selected. Need a productId or productCode.',
        }
        result = parse_error(error_xml)
        
        self.assertEquals(expected, result)
        
    def test_plans_parser(self):
        plans_xml = self.load_file('plans.xml')
        parser = PlansParser()
        
        expected = [   {   'billing_frequency': 'monthly',
                'billing_frequency_per': 'month',
                'billing_frequency_quantity': 1,
                'billing_frequency_unit': 'months',
                'code': 'FREE_MONTHLY',
                'created_datetime': datetime(2011, 1, 7, 20, 46, 43, tzinfo=tzutc()),
                'description': 'A free monthly plan',
                'id': '6b0d13f4-6bef-102e-b098-40402145ee8b',
                'is_active': True,
                'is_free': True,
                'name': 'Free Monthly',
                'recurring_charge_amount': Decimal('0.00'),
                'recurring_charge_code': 'FREE_MONTHLY_RECURRING',
                'setup_charge_amount': Decimal('0.00'),
                'setup_charge_code': '',
                'trial_days': 0},
            {   'billing_frequency': 'monthly',
                'billing_frequency_per': 'month',
                'billing_frequency_quantity': 1,
                'billing_frequency_unit': 'months',
                'code': 'PAID_MONTHLY',
                'created_datetime': datetime(2011, 1, 7, 21, 5, 42, tzinfo=tzutc()),
                'description': '',
                'id': '11af9cfc-6bf2-102e-b098-40402145ee8b',
                'is_active': True,
                'is_free': False,
                'name': 'Paid Monthly',
                'recurring_charge_amount': Decimal('20.00'),
                'recurring_charge_code': 'PAID_MONTHLY_RECURRING',
                'setup_charge_amount': Decimal('0.00'),
                'setup_charge_code': '',
                'trial_days': 0}]
        result = parser.parse_xml(plans_xml)
        
        self.assertEquals(expected, result)
        
    def test_customers_parser(self):
        customers_xml = self.load_file('customers.xml')
        parser = CustomersParser()
        
        result = parser.parse_xml(customers_xml)
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(result)
        
        #assert False
        
        