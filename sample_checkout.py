from magicway_payment_gateway import MoMagic

settings = {
    'store_id': '********',
    'store_secret': '********',
    'store_username': '********',
    'store_email': '********',
    'is_sandbox': True
}
mmbd_connector = MoMagic(settings)
# Organize the checkout data and all fields must be filled up proper value
checkout_data = {
    'currency': "BDT",
    'amount': "10.00",  # amount must be greater than or equal to 10
    'cus_name': "arifur rahman",
    'email': "arif.cuet017@gmail.com",
    'msisdn': "01811989965",
    'cus_country': "BD",
    'cus_state': "UNKNOWN",
    'cus_city': "UNKNOWN",
    'cus_postcode': "UNKNOWN",
    'cus_address': "UNKNOWN",
    'product_name': "UNKNOWN",
    'num_of_item': 1,
    "success_url": "UNKNOWN",
    "fail_url": "UNKNOWN",
    "cancel_url": "UNKNOWN",
    "ipn_url": "UNKNOWN"
}
print(mmbd_connector.checkout(checkout_data))
