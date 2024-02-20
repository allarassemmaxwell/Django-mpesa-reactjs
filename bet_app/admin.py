# Register your models here.
from django.contrib import admin
from .models import Bet, Transaction

admin.site.register(Bet)
admin.site.register(Transaction)
