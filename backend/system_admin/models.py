from django.db import models

# Create your models here.
class FraudDetectionSDKUser(models.Model):
    external_user_id = models.CharField(max_length=255, unique=True, help_text='The ID from the fintech app')
    risk_score = models.IntegerField(default=0, help_text='Calculated score from 0 10 100')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.external_user_id} (Risk: {self.risk_score})'
    
class DeviceFingerprint(models.Model):
    user = models.ForeignKey(FraudDetectionSDKUser, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255, unique=True, help_text='Unique hardware ID from flutter')
    os_name = models.CharField(max_length=50, help_text='IOS or Android')
    os_version = models.CharField(max_length=20)
    device_model = models.CharField(max_length=100, help_text='e.g. iPhone 15, Pixel 8')
    is_rooted_or_jailbroken = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_model} {self.os_name}'

class FraudDetectionSDKTimelineEvent(models.Model):
    EVENT_TYPES = [
        ('LOGIN', 'User Login'),
        ('TRANSFER', 'Money Transfer'),
        ('PROFILE_UPDATE', 'Profile Update'),
        ('SUSPICIOUS_BEHAVIOR', 'Suspicious Behavior')
    ]

    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk')
    ]

    user = models.ForeignKey(FraudDetectionSDKUser, on_delete=models.CASCADE, related_name='events')
    device = models.ForeignKey(DeviceFingerprint, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField(help_text='Human-readable detail for admin timeline')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location_city = models.CharField(max_length=100, null=True, blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='LOW')
    paste_detected = models.BooleanField(default=True, help_text='True if they pasted the text instead of typing')
    typing_speed_cps = models.FloatField(null=True, blank=True, help_text='Characters per second')
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.event_type} by {self.user.external_user_id} at {self.timestamp}'
