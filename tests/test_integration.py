from decimal import Decimal

import pytest
from django.db import connection
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import Transaction, Wallet


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Setup the test database with necessary privileges."""
    import mysql.connector

    connection = mysql.connector.connect(host="db", user="root", password="mypassword")
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_mydatabase;")
    cursor.execute("GRANT ALL PRIVILEGES ON test_mydatabase.* TO 'myuser'@'%';")
    cursor.execute("FLUSH PRIVILEGES;")
    cursor.close()
    connection.close()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def clean_database():
    """Clean the database before each test."""
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for table in connection.introspection.table_names():
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


@pytest.mark.django_db
def test_wallet_creation(api_client):
    response = api_client.post(reverse("wallet-list"), {"label": "Test Wallet"})
    assert response.status_code == 201
    assert Wallet.objects.count() == 1


@pytest.mark.django_db
def test_transaction_creation(api_client):
    wallet = Wallet.objects.create(label="Test Wallet")
    response = api_client.post(
        reverse("transaction-list"),
        {"wallet_id": wallet.id, "txid": "12345", "amount": "100.00"},
    )
    assert response.status_code == 201
    assert Transaction.objects.count() == 1


@pytest.mark.django_db
def test_wallet_balance_update(api_client):
    wallet = Wallet.objects.create(label="Test Wallet")
    api_client.post(
        reverse("transaction-list"),
        {"wallet_id": wallet.id, "txid": "12345", "amount": "100.00"},
    )
    wallet.refresh_from_db()
    assert wallet.balance == Decimal("100.00")


@pytest.mark.django_db
def test_get_wallets(api_client):
    Wallet.objects.create(label="Wallet 1")
    Wallet.objects.create(label="Wallet 2")
    Wallet.objects.create(label="Wallet 3")

    response = api_client.get(reverse("wallet-list"))
    assert response.status_code == 200
    assert len(response.data) == 3

    response = api_client.get(reverse("wallet-list") + "?label=Wallet 1")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["label"] == "Wallet 1"


@pytest.mark.django_db
def test_get_transactions(api_client):
    wallet = Wallet.objects.create(label="Test Wallet")
    Transaction.objects.create(wallet=wallet, txid="tx1", amount=Decimal("100.00"))
    Transaction.objects.create(wallet=wallet, txid="tx2", amount=Decimal("200.00"))
    Transaction.objects.create(wallet=wallet, txid="tx3", amount=Decimal("300.00"))

    response = api_client.get(reverse("transaction-list"))
    assert response.status_code == 200
    assert len(response.data) == 3

    response = api_client.get(reverse("transaction-list") + "?txid=tx1")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["txid"] == "tx1"

    response = api_client.get(reverse("transaction-list") + f"?wallet_id={wallet.id}")
    assert response.status_code == 200
    assert len(response.data) == 3
