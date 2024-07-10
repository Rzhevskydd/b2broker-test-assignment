from rest_framework import viewsets

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
