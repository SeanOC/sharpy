from sharpy.product import CheddarProduct

# Get a product instance to work with
product = CheddarProduct(
    username = CHEDDAR_USERNAME,
    password = CHEDDAR_PASSWORD,
    product_code = CHEDDAR_PRODUCT,
)

# Create the customer
customer = product.create_customer(
    code = 'cust-id-2',
    first_name = 'Turanga',
    last_name = 'Leela',
    email = 'tleela@planetexpress.com',
    plan_code = 'PAID_MONTHLY',
    
    method = 'paypal',
    
    cc_first_name = 'Hubert',
    cc_last_name = 'Farnsworth',
    
    return_url = 'https://www.planetexpress.com/thanks/cust-id-2/',
    cancel_url = 'https://www.planetexpress.com/sorry/cust-id-2/',
)
# redirect the user to the Paypal site to authorize the subscription
redirect(
    customer.subscriptions[0].redirect_url,
)
