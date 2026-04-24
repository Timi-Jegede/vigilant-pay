from django.db import models
from django.contrib.auth.models import User
from urllib.parse import quote
import base64
from django.conf import settings
from cryptography.fernet import Fernet
from .services import UserService
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    mfa_configured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}' Profile"

    def secret_key(self):
        fernet_key = settings.FERNET_KEY
        fernet_decryption = Fernet(fernet_key)
        
        encrypted_from_db = self.otp_secret
        decrypted_secret_key = fernet_decryption.decrypt(encrypted_from_db.encode())
        decoded_secret_key = decrypted_secret_key.decode()

        return decoded_secret_key

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')
    masked_card = models.CharField(max_length=20)
    card_hash = models.CharField(max_length=64, db_index=True)
    expiry_date = models.DateField()
    cardholder = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    location = models.CharField()
    merchant_type = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    transaction_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save_user_transaction(self, cardholder, raw_card_number, expiry_date, amount, currency, 
                              location, merchant_type, ip_address, transaction_date):
        processed_user_card = UserService().process_user_card(raw_card_number)
        
        self.masked_card = processed_user_card['masked_number']
        self.card_hash = processed_user_card['card_hash']
        self.cardholder = cardholder

        if isinstance(expiry_date, str) and '/' in expiry_date:
            try:
                self.expiry_date = datetime.strptime(expiry_date, '%m/%y').date()
            except ValueError:
                pass

        self.amount = amount
        self.currency = currency
        self.location = location
        self.merchant_type = merchant_type
        self.ip_address = ip_address

        native_datetime = datetime.strptime(transaction_date, '%Y-%m-%d').replace(hour=12)
        localized_datetime = timezone.make_aware(native_datetime)
        self.transaction_date = localized_datetime

        self.save()

        return f'Saved transaction for {self.user.username}, field {self.id}'

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
