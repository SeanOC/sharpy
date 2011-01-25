from datetime import datetime, timedelta

from sharpy.product import CheddarProduct

# Get a product instance to work with
product = CheddarProduct(
    username = CHEDDAR_USERNAME,
    password = CHEDDAR_PASSWORD,
    product_code = CHEDDAR_PRODUCT,
)

# Set a intitial bill date in the future to provide a free trial
bill_date = datetime.now() + timedelta(days=60)

# Create the customer
customer = product.create_customer(
    # Required fields
    code = 'cust-id-3',
    first_name = 'Hermes',
    last_name = 'Conrad',
    email = 'hconrad@planetexpress.com',
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

    # Optional Fields
    initial_bill_date = bill_date,
    referer = 'http://www.momsfriendlyrobots.com/',
)