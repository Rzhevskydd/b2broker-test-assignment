from django.db import models

class Wallet(models.Model):
    label = models.CharField(max_length=255, db_index=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE, db_index=True)
    txid = models.CharField(max_length=255, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
