from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from .models import Bet, Transaction
from .views import deposit

# Assuming MpesaAPI is the class you're mocking
from .mpesa_api import MpesaAPI


class DepositTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.bet = Bet.objects.create(phone_number="+1234567890", amount=100)

    def test_deposit_success(self):
        # Mock the MpesaAPI deposit method to return a successful response
        with patch.object(MpesaAPI, 'deposit', return_value={"success": True}):
            response = self.client.post(
                reverse('deposit'),
                {"bet_id": self.bet.id, "amount": 100}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['message'], "Deposit successful")
            self.assertTrue(Transaction.objects.filter(
                bet=self.bet, transaction_type="deposit", amount=100).exists())

    def test_deposit_failure(self):
        # Mock the MpesaAPI deposit method to return a failed response
        with patch.object(MpesaAPI, 'deposit', return_value={"success": False}):
            response = self.client.post(
                reverse('deposit'),
                {"bet_id": self.bet.id, "amount": 100}
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['error'], "Deposit failed")
            self.assertFalse(Transaction.objects.filter(
                bet=self.bet, transaction_type="deposit", amount=100).exists())

    def test_deposit_invalid_bet(self):
        response = self.client.post(
            reverse('deposit'),
            {"bet_id": self.bet.id + 1, "amount": 100}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], "Bet not found")

    def test_deposit_invalid_request(self):
        response = self.client.get(reverse('deposit'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], "Invalid request")
