from sharpy.product import CheddarProduct

# Get a product instance to work with
product = CheddarProduct(
    username = CHEDDAR_USERNAME,
    password = CHEDDAR_PASSWORD,
    product_code = CHEDDAR_PRODUCT,
)

# Get the customer from Cheddar Getter
customers = product.get_customers()