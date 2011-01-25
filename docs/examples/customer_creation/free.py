from sharpy.product import CheddarProduct

# Get a product instance to work with
product = CheddarProduct(
    username = CHEDDAR_USERNAME,
    password = CHEDDAR_PASSWORD,
    product_code = CHEDDAR_PRODUCT,
)

# Create the customer
customer = product.create_customer(
    code = 'cust-id-1', # An unique identifier for the customer
    first_name = 'Philip',
    last_name = 'Fry',
    email = 'pfry@planetexpress.com',
    plan_code = 'FREE_MONTHLY', # The code for plan to subscribe the customer to
)