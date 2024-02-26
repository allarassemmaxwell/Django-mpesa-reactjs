from django.shortcuts import render
from .serializers import *   
from .models import * 
from rest_framework import status
from rest_framework.response import  Response
from rest_framework.decorators import api_view
from django.conf import settings

from decimal import Decimal

import requests
from requests.auth import HTTPBasicAuth
import json
from .utils import *










# Home view


def home(request):
    return render(request, "home.html")



# =========================================================
#                     USER DEPOSIT
# =========================================================
@api_view(['POST'])
def Deposit(request):
    if request.method == 'POST':
        serializer = DepositeSerializer(data=request.data)
        if serializer.is_valid():
            amount  = 1 # Decimal(serializer.data.get("amount"))
            phone   = str(request.user.phone_number)
            phone_number  = str(country+phone)[1:]
            query_payload = {
                "BusinessShortCode": settings.MPESA_SHORT_CODE,    
                "Password": mpesa_password(),    
                "Timestamp": mpesa_timestamp(),    
                "TransactionType": settings.MPESA_SHORTCODE_TYPE,    
                "Amount": int(amount),    
                "PartyA": phone_number,    
                "PartyB": settings.MPESA_SHORT_CODE,    
                "PhoneNumber": phone_number,    
                "CallBackURL": settings.MPESA_DEPOSITE_RESULT_URL,    
                "AccountReference":"Test",    
                "TransactionDesc":"Test"
            }
            query_headers = {'Authorization': 'Bearer ' + get_mpesa_token(), 'Content-Type': 'application/json'}
            response = requests.post(settings.MPESA_DEPOSITE_URL, json=query_payload, headers=query_headers)
            return HttpResponse(response.text)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












# =========================================================
#                  USER DEPOSIT RESULT
# =========================================================
@api_view(['POST'])
def DepositResult(request):
    if request.method == 'POST':
        data = request.data
        ResultCode = data['Body']['stkCallback']['ResultCode']
        if ResultCode == 0:
            amount              = 1000 # data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
            reference           = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
            phone               = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
            merchant_request_id = data['Body']['stkCallback']['MerchantRequestID']
            checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
            result_code         = data['Body']['stkCallback']['ResultCode']
            phone_number = int(str(phone)[3:])

            Transaction.objects.create(
                phone_number                = phone_number,
                transaction_type    = "deposit",
                payment_method      = "MPESA",
                reference           = reference,
                result_code         = result_code,
                merchant_request_id = merchant_request_id,
                checkout_request_id = checkout_request_id,
                amount              = amount
            )
            message = data['Body']['stkCallback']['ResultDesc']
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = data['Body']['stkCallback']['ResultDesc']
            return Response(message, status=status.HTTP_400_BAD_REQUEST)









# =========================================================
#                     MPESA WITHDRAW
# =========================================================
@api_view(['POST'])
def Withdraw(request):
    if request.method == 'POST':
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount  = Decimal(serializer.data.get("amount"))
            phone   = str(request.user.phone_number)
            phone_number  = 254708374149 # str(country+phone)[1:]
            if amount < 50:
                message = {"Minimum amount per request is 50.00 KES."}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            elif amount > request.user.balance:
                message = {"Amount must be less than balance."}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            query_payload = {
                "OriginatorConversationID": random_string(36),
                "InitiatorName": settings.MPESA_INITIATOR_USERNAME,
                "SecurityCredential": settings.MPESA_SECURITY_CREDENTIAL,
                "CommandID": "BusinessPayment",
                "Amount": int(amount),
                "PartyA": settings.MPESA_B2C_PARTY_A,
                "PartyB": phone_number,
                "Remarks": "Test remarks",
                "QueueTimeOutURL": "https://04da-41-90-187-151.ngrok-free.app/api/user/withdraw/timeout/",
                "ResultURL": "https://04da-41-90-187-151.ngrok-free.app/api/user/withdraw/result/",
                "Occasion": "Christmas",
            }
            query_headers = {'Authorization': 'Bearer ' + get_mpesa_token(), 'Content-Type': 'application/json'}
            response = requests.post(settings.MPESA_WITHDRAW_URL, json=query_payload, headers=query_headers)
            return HttpResponse(response.text)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












# =========================================================
#                  MPESA WITHDRAW RESULT
# =========================================================
@api_view(['POST'])
def WithdrawResult(request):
    if request.method == 'POST':
        data = request.data
        ResultCode = data['Result']['ResultCode']
        if ResultCode   == 0:
            result_code         = data['Result']['ResultCode']
            ori_conversation_id = data['Result']['OriginatorConversationID']
            conversation_id     = data['Result']['ConversationID']
            amount              = data['Result']['ResultParameters']['ResultParameter'][0]['Value']
            reference           = data['Result']['ResultParameters']['ResultParameter'][1]['Value']
            phone               = data['Result']['ResultParameters']['ResultParameter'][2]['Value'][0:12]
            phone_number        = 711898366 # int(str(phone)[3:])

            Transaction.objects.create(
                phone_number        = phone_number,
                transaction_type    = "withdraw",
                payment_method      = "MPESA",
                reference           = reference,
                result_code         = result_code,
                ori_conversation_id = ori_conversation_id,
                conversation_id     = conversation_id,
                amount              = amount
            )
            message = data['Result']['ResultDesc']
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = data['Result']['ResultDesc']
            return Response(message, status=status.HTTP_400_BAD_REQUEST)














# =========================================================
#                MPESA WITHDRAW TIME OUT
# =========================================================
@api_view(['POST'])
def WithdrawTimeOut(request):
    if request.method == 'POST':
        data    = request.data
        message = {"Time out."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)








