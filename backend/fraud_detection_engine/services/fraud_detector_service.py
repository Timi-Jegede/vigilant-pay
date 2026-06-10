import secrets
import string
from django.core.cache import caches
from ..alert_service import EmailService

class FraudDetectorService:
    @staticmethod
    def trigger_sms(user_id, user_email, transaction_data, length=6):
        allowed_characters = string.digits
        otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))

        redis_key = f'otp:user:{user_id}'
        redis_cache = caches['default']
        redis_cache.set(redis_key, otp, timeout=300)

        sent_email = EmailService().send_fraud_alert(user_email, transaction_data)

        if sent_email:
            return True

