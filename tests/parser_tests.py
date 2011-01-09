from datetime import datetime
from decimal import Decimal
import os
import unittest

from dateutil.tz import tzutc
from nose.tools import raises

from sharpy.exceptions import ParseError
from sharpy.parsers import CheddarOutputParser

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
        
    def test_int_parsing(self):
        parser = CheddarOutputParser()
        
        expected = 234
        result = parser.parse_int('234')
        
        self.assertEquals(expected, result)
        
    @raises(ParseError)
    def test_int_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_int('test')
        
    def test_decimal_parsing(self):
        parser = CheddarOutputParser()
        
        expected = Decimal('2.345')
        result = parser.parse_decimal('2.345')
        
        self.assertEquals(expected, result)
    
    @raises(ParseError)
    def test_decimal_parsing_error(self):
        parser = CheddarOutputParser()
        
        parser.parse_decimal('test')
        
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