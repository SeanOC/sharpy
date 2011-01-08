from copy import copy
import unittest

from nose.tools import raises
from testconfig import config

from sharpy.client import Client
from sharpy.exceptions import AccessDenied, BadRequest, NotFound

from testing_tools.decorators import clear_users

class ClientTests(unittest.TestCase):
    client_defaults =  {
        'username': config['cheddar']['username'],
        'password': config['cheddar']['password'],
        'product_code': config['cheddar']['product_code'],
    }
    
    def get_client(self, **kwargs):
        client_kwargs = copy(self.client_defaults)
        client_kwargs.update(kwargs)
        
        c = Client(**client_kwargs)
        
        return c
    
    def try_client(self, **kwargs):
        args = copy(self.client_defaults)
        args.update(kwargs)
        client = self.get_client(**kwargs)
        
        self.assertEquals(args['username'], client.username)
        self.assertEquals(self.client_defaults['password'] ,client.password)
        self.assertEquals(self.client_defaults['product_code'], client.product_code)
        if 'endpoint' in args.keys():
            self.assertEquals(args['endpoint'], client.endpoint)
        else:
            self.assertEquals(client.default_endpoint, client.endpoint)
    
    def test_basic_init(self):
        self.try_client()
        
    def test_custom_endpoint_init(self):
        self.try_client(endpoint = 'http://cheddar-test.saaspire.com')
        
    
    def try_url_build(self, path, params=None):
        c = self.get_client()
        expected = u'%s/%s/productCode/%s' % (
            c.default_endpoint,
            path,
            c.product_code,
        )
        if params:
            for key, value in params.items():
                expected = u'%s/%s/%s' % (expected, key, value)

        result = c.build_url(path=path, params=params)

        self.assertEquals(expected, result)
        
    def test_basic_build_url(self):
        path = 'users'
        self.try_url_build(path)
        
    
    def test_single_param_build_url(self):
        path = 'users'
        params = {'key': 'value'}
        self.try_url_build(path, params)
        
    def test_multi_param_build_url(self):
        path = 'users'
        params = {'key1': 'value1', 'key2': 'value2'}
        self.try_url_build(path, params)
        
    def test_make_request(self):
        path = 'plans/get'
        client = self.get_client()
        response, content = client.make_request(path)
        
        self.assertEquals(response.status, 200)
    
    @raises(AccessDenied)
    def test_make_request_access_denied(self):
        path = 'plans/get'
        bad_username = self.client_defaults['username'] + '_bad'
        client = self.get_client(username=bad_username)
        client.make_request(path)
        
    @raises(BadRequest)
    def test_make_request_bad_request(self):
        path = 'plans'
        client = self.get_client()
        client.make_request(path)
        
    @raises(NotFound)
    def test_make_request_not_found(self):
        path = 'things-which-dont-exist'
        client = self.get_client()
        client.make_request(path)
        