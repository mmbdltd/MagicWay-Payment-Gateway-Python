### MagicWay Payment Gateway Integration - Python  Package

Note: If you're using this package with our sandbox environment is_sandbox is True and live is_sandbox is False.
Please contact info@momagicbd.com to get credentials.

### Package Directory

```
 |-- magicway_payment_gateway/
    |-- __init__.py
    |-- momagic_connector.py (core file)
    |-- status_code.py (core file)
 |-- sample_checkout.py
 |-- sample_ipn.py
 |-- setup.py
 |-- LICENSE
 |-- README.md
 |-- .gitignore
```

# Installation

pip install magicway-payment-gateway

### Usage

Sample Payment Session API example:

from magicway_payment_gateway import MoMagic

settings = {
    'store_id': '**********',
    'store_secret': '**********',
    'store_username': '**********',
    'store_email': '**********',
    'is_sandbox': True
}

mmbd_connector = MoMagic(settings)

# Organize the checkout data and all fields must be filled up proper value

checkout_data = {
    'currency': "BDT",
    'amount': "10.00",  # amount must be greater than or equal to 10
    'cus_name': "test name",
    'email': "test@test.com",
    'msisdn': "01800000000",
    'cus_country': "BD",
    'cus_state': "customer state",
    'cus_city': "customer city",
    'cus_postcode': "customer postcode",
    'cus_address': "customer address",
    'product_name': "product name",
    'num_of_item': 1,
    "success_url": "success url",
    "fail_url": "fail url",
    "cancel_url": "cancel url",
    "ipn_url": "ipn url"
}

response=mmbd_connector.checkout(checkout_data)

print(response)

# response['status_code'] == 200, Need to customer post redirection response['checkout_url']  and save response['order_id'] for payment validation

Sample Payment Validation API example:

from magicway_payment_gateway import MoMagic

settings = {
    'store_id': '**********',
    'store_secret': '**********',
    'store_username': '**********',
    'store_email': '**********',
    'is_sandbox': True
}

mmbd_connector = MoMagic(settings)

# Organize the payment validation data

payment_validation_data = {
    'opr': "**********",
    'order_id': "**********",
    'reference_id': "**********"
}

response=mmbd_connector.instant_payment_notification(payment_validation_data)

print(response)

# If response['status_code'] == 200 and response['charge_status'], then we can decide transaction is successful

### Contributors

> Arifur Rahman

> info@momagicbd.com
