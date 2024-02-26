import requests
from datetime import datetime
import json
import base64
from django.http import JsonResponse, HttpResponse

from django.conf import settings

from requests.auth import HTTPBasicAuth



# =========================================================
#                    DARAJA GET TOKEN  
# =========================================================
def get_mpesa_token():
    response = requests.get(settings.MPESA_TOKEN_URL, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json()['access_token']

        




# =========================================================
#                    DARAJA FORMAT TIME 
# =========================================================
def mpesa_timestamp():
    unformated_datetime = datetime.now()
    formated_datetime   = unformated_datetime.strftime("%Y%m%d%H%M%S") 
    return formated_datetime




# =========================================================
#                 DARAJA GENERATE PASSWORD
# =========================================================
def mpesa_password():
    password_str   = settings.MPESA_SHORT_CODE + settings.MPESA_PASSKEY + mpesa_timestamp()
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")


