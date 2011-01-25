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
    cc_number = '4111111111111111',
    cc_expiration = '03/3012',
    cc_card_code = '123',
    cc_first_name = 'Hubert',
    cc_last_name = 'Farnsworth',
    cc_address = '1 πth Ave.',
    cc_city = 'New New York',
    cc_state = 'New York',
    cc_zip = '10001',
)