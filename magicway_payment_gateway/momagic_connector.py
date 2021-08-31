def get_date(date_format):
    import datetime
    date_obj = datetime.datetime.now()
    return date_obj.strftime(date_format)


def generate_random_uuid(length=20):
    import uuid
    # generate random uid and convert to string
    uid = uuid.uuid4().hex[:length]
    # print("uid :", uid, "length :", len(uid))
    return uid


class MoMagic(object):
    __store_id = None
    __store_secret = None
    __grant_type = 'password'
    __store_username = None
    __store_email = None
    __is_sandbox = None
    __mode = None
    __payment_initiator_url = None
    __access_token_url = None
    __payment_validation_url = None
    __authentication_header = {}

    def __init__(self, config):
        self.__store_id = config['store_id']
        self.__store_secret = config['store_secret']
        self.__store_username = config['store_username']
        self.__store_email = config['store_email']
        self.__mode = 'sandbox' if (config['is_sandbox']) else 'securepay'
        self.__payment_initiator_url = "https://" + self.__mode + ".magicway.io/api/V1/payment-initiate"
        self.__access_token_url = "https://" + self.__mode + ".magicway.io/api/V1/auth/token"
        self.__payment_validation_url = "https://" + self.__mode + ".magicway.io/api/V1/charge/status"

    def __set_authentication_headers(self, token=None):
        # self.__authentication_header['content-type'] = "application/json"
        if token:
            self.__authentication_header['Authorization'] = 'Bearer ' + token

    def __get_authentication_header(self):
        return self.__authentication_header

    def __do_api_call(self, method, url, payload):
        import requests
        headers = self.__get_authentication_header()
        # print("headers :", headers)
        try:
            if method == 'POST':
                response = requests.post(url, data=payload, headers=headers)
            else:
                response = {'response': 'Method is not valid'}
            return response
        except Exception as error:
            # print("error", error)
            response = {'response': error}
            return response

    def __access_token(self):
        authentication_data = {
            'store_id': self.__store_id,
            'grant_type': self.__grant_type,
            'store_secret': self.__store_secret,
            'username': self.__store_username,
            'email': self.__store_email
        }
        api_url = self.__access_token_url
        response = self.__do_api_call('POST', api_url, authentication_data)
        return response

    def __payment_checkout(self, checkout_data):
        checkout_data['store_id'] = self.__store_id
        checkout_data['order_id'] = generate_random_uuid(20)
        # print("order_id :", checkout_data['order_id'])
        api_url = self.__payment_initiator_url
        response = self.__do_api_call('POST', api_url, checkout_data)
        return response

    def __payment_validator(self, payment_validation_data):
        payment_validation_data['store_id'] = self.__store_id
        api_url = self.__payment_validation_url
        response = self.__do_api_call('POST', api_url, payment_validation_data)
        return response

    def checkout(self, checkout_data):
        from .status_code import INTERNAL_ERROR, ALL_OK
        response = {}
        try:
            # call the checkout API
            api_response = self.__payment_checkout(checkout_data)
            api_status_code = api_response.status_code
            # print("api_response_status", api_status_code)
            if api_status_code != ALL_OK:
                # api_response = api_response.text
                raise MyException(
                    {"message": 'FAILED TO CONNECT WITH MagicWay PAYMENT CHECKOUT API', "status_code": api_status_code})
            else:
                api_response = api_response.json()
            # print("api_response", api_response)
            if api_response["success"] and api_response["status_code"] == ALL_OK:
                response['status_code'] = ALL_OK
                response['order_id'] = api_response["order_id"]
                response['checkout_url'] = api_response["checkout_url"]
            else:
                raise MyException({"message": api_response["message"], "status_code": api_response["status_code"]})
        except MyException as exp_obj:
            # print("Custom Exception MSG :", exp_obj)
            response['message'] = exp_obj.message
            response['status_code'] = exp_obj.status_code
        except Exception as e:
            # print("Exception MSG :", e)
            response['message'] = str(e)
            response['status_code'] = INTERNAL_ERROR
        finally:
            return response

    def instant_payment_notification(self, payment_data):
        from .status_code import INTERNAL_ERROR, ALL_OK
        response = {
            'charge_status': False
        }
        try:
            # call the access token API
            access_token_response = self.__access_token()
            access_token_api_status = access_token_response.status_code
            # print("access_token_api_status", access_token_api_status)
            access_token_response = access_token_response.text if access_token_api_status != ALL_OK else access_token_response.json()
            # print("access_token_response", access_token_response)
            if access_token_api_status != ALL_OK:
                raise MyException(
                    {"message": 'FAILED TO CONNECT WITH MagicWay ACCESS TOKEN API',
                     "status_code": access_token_api_status})
            elif access_token_response["success"] and access_token_response["status_code"] == ALL_OK:
                # token will be used for authorization
                token = access_token_response["access_token"]
                self.__set_authentication_headers(token)
                # set the below dictionary data from API request data
                payment_validation_payload = {
                    'opr': payment_data['opr'],
                    'order_id': payment_data['order_id'],
                    'reference_id': payment_data['reference_id'],
                    'is_plugin': 'YES'
                }
                payment_validation_response = self.__payment_validator(payment_validation_payload)
                payment_validation_api_status = payment_validation_response.status_code
                # print("payment_validation_api_status", payment_validation_api_status)
                payment_validation_response = payment_validation_response.text if payment_validation_api_status != ALL_OK else payment_validation_response.json()
                # print("payment_validation_response", payment_validation_response)
                if payment_validation_api_status != ALL_OK:
                    raise MyException({"message": 'FAILED TO CONNECT WITH MagicWay PAYMENT VALIDATION API',
                                       "status_code": payment_validation_api_status})
                elif payment_validation_response["success"] and payment_validation_response["status_code"] == ALL_OK:
                    payment_status = True if payment_validation_response["charge_status"] == "Success" else False
                    # ecommerce_order_id = payment_validation_response.get('ecom_order_id')
                    # print("payment_status :", payment_status)
                    response['status_code'] = ALL_OK
                    response['charge_status'] = payment_status
                else:
                    raise MyException({"message": payment_validation_response['message'],
                                       "status_code": payment_validation_response["status_code"]})
            else:
                raise MyException(
                    {"message": access_token_response["message"], "status_code": access_token_response["status_code"]})
        except MyException as exp_obj:
            # print("Custom Exception MSG :", exp_obj)
            response['message'] = exp_obj.message
            response['status_code'] = exp_obj.status_code
        except Exception as e:
            # print("Exception MSG :", e)
            response['message'] = str(e)
            response['status_code'] = INTERNAL_ERROR
        finally:
            return response


class MyException(Exception):
    message = None
    status_code = None

    def __init__(self, data):
        self.message = data['message']
        self.status_code = data['status_code']
