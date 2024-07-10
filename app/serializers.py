from rest_framework import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all())

    class Meta:
        model = Transaction
        fields = ["id", "wallet", "txid", "amount"]
