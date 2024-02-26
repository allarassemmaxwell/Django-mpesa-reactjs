# Create your models here.
from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from decimal import Decimal
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def validate_phone_number(value):
    phone = str(value)
    if len(phone) < 9 or len(phone) > 10:
        raise ValidationError(
            _('Must be a valid mobile number'),
            params={'value': value},
        )




TRANSACTION_TYPES = (
    ('deposit', 'deposit'),
    ('withdraw', 'withdraw'),
)

class Transaction(models.Model):
    id               = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    phone_number     = models.PositiveIntegerField(_("Phone Number"), null=False, blank=False, validators=[validate_phone_number])
    transaction_type = models.CharField(_("Type"), max_length=20, choices=TRANSACTION_TYPES, null=False, blank=False)
    transaction_id   = models.CharField(_("Transaction ID"), max_length=255, null=True, blank=False)
    result_code      = models.PositiveIntegerField(_("Result Code"), null=True, blank=True)
    merchant_request_id = models.CharField(_("Merchant Request ID"), max_length=255, null=True, blank=True)
    checkout_request_id = models.CharField(_("Checkout Request ID"), max_length=255, null=True, blank=True)
    ori_conversation_id = models.CharField(_("Originator Conversation ID"), max_length=255, null=True, blank=True)
    conversation_id  = models.CharField(_("Conversation ID"), max_length=255, null=True, blank=True)
    amount           = models.DecimalField(_("Amount"), decimal_places=2, max_digits=15, null=False, blank=False, validators=[MinValueValidator(Decimal('00.00'))])
    timestamp        = models.DateTimeField(_("Created At"), auto_now_add=True, auto_now=False)
    updated          = models.DateTimeField(_("Updated At"), auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.phone_number)

    def clean(self):
        transaction_type = self.transaction_type
        payment_method   = self.payment_method
        amount           = self.amount

        if transaction_type != "deposit" and transaction_type != "withdraw":
            raise ValidationError({"transaction_type": _("Transaction type not allowed")})
        elif transaction_type == "deposit" and amount < 10:
            raise ValidationError({"amount": "Minimum amount per request is 10.00 KES."}) 
        elif transaction_type == "withdraw" and amount < 50:
            raise ValidationError({"amount": "Minimum amount per request is 50.00 KES."})

    class Meta:
        ordering = ("-timestamp",)
        # verbose_name_plural = _("Countries")










