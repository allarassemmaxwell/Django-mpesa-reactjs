# Generated by Django 4.2.10 on 2024-02-23 23:03

import bet_app.models
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "phone_number",
                    models.PositiveIntegerField(
                        validators=[bet_app.models.validate_phone_number],
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("deposit", "deposit"), ("withdraw", "withdraw")],
                        max_length=20,
                        verbose_name="Type",
                    ),
                ),
                (
                    "transaction_id",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Transaction ID"
                    ),
                ),
                (
                    "result_code",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Result Code"
                    ),
                ),
                (
                    "merchant_request_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Merchant Request ID",
                    ),
                ),
                (
                    "checkout_request_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Checkout Request ID",
                    ),
                ),
                (
                    "ori_conversation_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Originator Conversation ID",
                    ),
                ),
                (
                    "conversation_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Conversation ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                        verbose_name="Amount",
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
            ],
            options={
                "ordering": ("-timestamp",),
            },
        ),
    ]
