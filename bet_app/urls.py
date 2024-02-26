from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('deposit/', Deposit, name='deposit'),
    path('deposit/result/', DepositResult, name="deposit_result"),
    path('withdraw/', Withdraw, name='withdraw'),
    path('withdraw/result/', WithdrawResult, name="withdraw_result"),
    path('withdraw/timeout/', WithdrawTimeOut, name="withdraw_timeout"),
]
