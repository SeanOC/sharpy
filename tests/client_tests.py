import unittest

from sharpy.client import Client

class ClientTests(unittest.TestCase):
    
    def try_client(self, username, password, product_code, endpoint=None):
        kwargs = {
            'username': 'user',
            'password': 'pass',
            'product_code': 'CODE',
        }
        if endpoint:
            kwargs['endpoint'] = endpoint
        
        client = Client(**kwargs)
        
        self.assertEquals(username, client.username)
        self.assertEquals(password, client.password)
        self.assertEquals(product_code, client.product_code)
        if endpoint:
            self.assertEquals(endpoint, client.endpoint)
        else:
            self.assertEquals(client.default_endpoint, client.endpoint)
    
    def test_basic_init(self):
        self.try_client(
            username = 'user',
            password = 'pass',
            product_code = 'CODE',
        )
        
    def test_custom_endpoint_init(self):
        self.try_client(
            username = 'user',
            password = 'pass',
            product_code = 'CODE',
            endpoint = 'http://cheddar-test.saaspire.com',
        )