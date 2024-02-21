# Create your models here.
from django.db import models


# BET Model where a user will use his phone number

class Bet(models.Model):
    phone_number = models.CharField(max_length=15)
    reference = models.CharField(max_length=200, blank=True, default='')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Bet by {self.phone_number} for {self.amount}'


# TRANSACTION Model to help a user make his transaction
class Transaction(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} for bet {self.bet.id}'
