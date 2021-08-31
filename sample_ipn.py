from magicway_payment_gateway import MoMagic

settings = {
    'store_id': '********',
    'store_secret': '********',
    'store_username': '********',
    'store_email': '********',
    'is_sandbox': True
}
mmbd_connector = MoMagic(settings)
# Organize the payment validation data
payment_validation_data = {
    'opr': "NAGAD",
    'order_id': "MTCG39380372",
    'reference_id': "MDgzMTExMTAwNjM4NS42ODc5ODA4NDMxNTUwNDUuTVRDRzM5MzgwMzcyLjc3Mjk2YzRkMzY5NTIyMTFhZTJi"
}
print(mmbd_connector.instant_payment_notification(payment_validation_data))