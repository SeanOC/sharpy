from sharpy.product import CheddarProduct
from sharpy import exceptions

# Get a product instance to work with
product = CheddarProduct(
    username = CHEDDAR_USERNAME,
    password = CHEDDAR_PASSWORD,
    product_code = CHEDDAR_PRODUCT,
)

try:
    # Get the customer from Cheddar Getter
    customer = product.get_customer(code='1BDI')
except exceptions.NotFound, err:
    print 'You do not appear to be a customer yet'
else:
    # Test if the customer's subscription is canceled
    if customer.subscription.canceled:
        if customer.subscription.cancel_type == 'paypal-pending':
            print 'Waiting for Paypal authorization'
        else:
            print 'Your subscription appears to have been cancelled'
    else:
        print 'Your subscription appears to be active'
