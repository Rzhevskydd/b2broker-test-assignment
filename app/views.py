from _decimal import Decimal
from django.db import transaction
from rest_framework import serializers, viewsets

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_fields = ["label"]
    search_fields = ["label"]
    ordering_fields = ["balance", "label"]
    ordering = ["label"]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ["wallet", "txid"]
    search_fields = ["txid"]
    ordering_fields = ["amount", "txid"]
    ordering = ["txid"]

    def perform_create(self, serializer):
        with transaction.atomic():
            transaction_instance = serializer.save()
            wallet = transaction_instance.wallet
            new_balance = wallet.balance + transaction_instance.amount
            if new_balance < Decimal("0.00"):
                raise serializers.ValidationError("Wallet balance cannot be negative.")
            wallet.balance = new_balance
            wallet.save()
