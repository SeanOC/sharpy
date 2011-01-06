class Client(object):
    default_endpoint = 'https://cheddargetter.com/xml'
    def __init__(self, username, password, product_code, endpoint=None):
        self.username = username
        self.password = password
        self.product_code = product_code
        self.endpoint = endpoint or self.default_endpoint
        
        super(Client, self).__init__()