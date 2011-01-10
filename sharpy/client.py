from urllib import urlencode

import httplib2

from sharpy.exceptions import CheddarError, AccessDenied, BadRequest, NotFound, PreconditionFailed, CheddarFailure, NaughtyGateway, UnprocessableEntity

class Client(object):
    default_endpoint = 'https://cheddargetter.com/xml'
    def __init__(self, username, password, product_code, cache=None, timeout=None, endpoint=None):
        '''
        username - Your cheddargetter username (probably an email address)
        password - Your cheddargetter password
        product_code - The product code for the product you want to work with
        cache - A file system path or an object which implements the httplib2
                cache API (optional)
        timeout - Socket level timout in seconds (optional)
        endpoint - An alternate API endpoint (optional)
        '''
        self.username = username
        self.password = password
        self.product_code = product_code
        self.endpoint = endpoint or self.default_endpoint
        self.cache = cache
        self.timeout = timeout
        
        super(Client, self).__init__()
    
    def build_url(self, path, params=None):
        '''
        Constructs the url for a cheddar API resource
        '''
        url = u'%s/%s/productCode/%s' % (
            self.endpoint,
            path,
            self.product_code,
        )
        if params:
            for key, value in params.items():
                url = u'%s/%s/%s' % (url, key, value)
            
        return url
    
    def make_request(self, path, params=None, data=None):
        '''
        Makes a request to the cheddar api using the authentication and 
        configuration settings available.
        '''
        # Setup values
        url = self.build_url(path, params)
        
        if data:
            method = 'POST'
            body = urlencode(data)
            headers = {
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
        else:
            method = 'GET'
            body = None
            headers = None
            
        # Setup http client
        h = httplib2.Http(cache=self.cache, timeout=self.timeout)
        h.add_credentials(self.username, self.password)
        
        # Make request
        response, content = h.request(url, method, body=body, headers=headers)
        status = response.status
        if status != 200:
            exception_class = CheddarError
            if status == 401:
                exception_class = AccessDenied
            elif status == 400:
                exception_class = BadRequest
            elif status == 404:
                exception_class = NotFound
            elif status == 412:
                exception_class = PreconditionFailed
            elif status == 500:
                exception_class = CheddarFailure
            elif status == 502:
                exception_class = NaughtyGateway
            elif status == 422:
                exception_class = UnprocessableEntity
            
            raise exception_class(response, content)
        
        response.content = content
        return response
        
        
