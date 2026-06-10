from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Feature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='features')
    probability = models.CharField(max_length=50)
    confidence_score = models.CharField(max_length=50)
    shap_values = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def save_transaction_prediction(self, probability, confidence_score, shap_values):
        self.probability = probability
        self.confidence_score = confidence_score
        self.shap_values = shap_values

        self.save()

class ClientPlatform(models.Model):
    company_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

class AccountEntity(models.Model):
    platform = models.ForeignKey(ClientPlatform, on_delete=models.CASCADE)
    external_account_id = models.CharField(max_length=255, db_index=True)
    identity_hash = models.CharField(max_length=64, db_index=True)
    trust_score = models.FloatField(default=1.0)
    precalculated_daily_average = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_blacklisted = models.BooleanField(default=False)

    class Meta:
            unique_together = ('platform', 'external_account_id')

    @classmethod
    def account_entity_records(cls, platform_id, external_account_id, identity_hash,
                               trust_score=1.0, precalculated_daily_average=0.00, is_blacklisted=False):
         record, created = cls.objects.get_or_create(
            platform_id = platform_id,
            external_account_id = external_account_id,
            defaults={
                'identity_hash': identity_hash,
                'trust_score': trust_score,
                'precalculated_daily_average': precalculated_daily_average,
                'is_blacklisted': is_blacklisted
            }
         )

         return record, created


class FinancialLegderEntry(models.Model):
    platform = models.ForeignKey(ClientPlatform, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    sender = models.ForeignKey(AccountEntity, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(AccountEntity, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    risk_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def financial_legder_entry_records(cls, platform_id, transaction_id, sender, receiver, amount,
                                       risk_score):
        cls.objects.create(
            platform_id = platform_id,
            transaction_id = transaction_id,
            sender = sender,
            receiver = receiver,
            amount = amount,
            risk_score = risk_score
        )

                                 