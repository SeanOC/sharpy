from datetime import datetime
from decimal import Decimal, InvalidOperation

from dateutil import parser as date_parser

try:
    from lxml.etree import XML
except ImportError:
    print "couldn't import LXML"
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