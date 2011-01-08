import httplib2
from testconfig import config

def clear_users():
    username = config['cheddar']['username']
    password = config['cheddar']['password']
    product = config['cheddar']['product_code']
    
    h = httplib2.Http()
    h.add_credentials(username, password)
    
    url = 'https://cheddargetter.com/xml/customers/delete-all/confirm/1/productCode/%s' % product
    
    response, content = h.request(url, 'POST')
    
    if response.status != 302:
        raise Exception('Could not clear users.  Recieved a response of %s %s ' % response.status, response.reason)