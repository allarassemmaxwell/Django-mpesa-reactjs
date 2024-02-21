# This is a placeholder for the actual Mpesa API integration
# from mpesa_api import MpesaAPI
from .models import Bet, Transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import *
from django.contrib import messages

from django.http import HttpResponse

# Create your views here.


# Home view


def home(request):
    return render(request, "home.html")


# To place a Bet


def place_bet(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        reference = request.POST.get("reference")
        amount = request.POST.get("amount")
        bet = Bet.objects.create(
            phone_number=phone_number, reference=reference, amount=amount
        )
        return JsonResponse({"message": "Bet placed successfully", "bet_id": bet.id})
    return JsonResponse({"error": "Invalid request"}, status=400)


# For deposit of the User
def deposit(request):
    if request.method == "POST":
        bet_id = request.POST.get("bet_id")
        amount = request.POST.get("amount")
        try:
            bet = Bet.objects.get(id=bet_id)
        except Bet.DoesNotExist:
            return JsonResponse({"error": "Bet not found"}, status=404)

        # Here you would integrate with the Mpesa API to make a deposit
        mpesa_api = MpesaAPI()
        response = mpesa_api.deposit(bet.phone_number, amount)

        if response["success"]:
            Transaction.objects.create(
                bet=bet, transaction_type="deposit", amount=amount
            )
            return JsonResponse({"message": "Deposit successful"})
        else:
            return JsonResponse({"error": "Deposit failed"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Help User to withdraw his money
def withdraw(request):
    if request.method == "POST":
        bet_id = request.POST.get("bet_id")
        amount = request.POST.get("amount")
        try:
            bet = Bet.objects.get(id=bet_id)
        except Bet.DoesNotExist:
            return JsonResponse({"error": "Bet not found"}, status=404)

        # Here you would integrate with the Mpesa API to make a withdrawal
        mpesa_api = MpesaAPI()
        response = mpesa_api.withdraw(bet.phone_number, amount)

        if response["success"]:
            Transaction.objects.create(
                bet=bet, transaction_type="withdraw", amount=amount
            )
            return JsonResponse({"message": "Withdrawal successful"})
        else:
            return JsonResponse({"error": "Withdrawal failed"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
