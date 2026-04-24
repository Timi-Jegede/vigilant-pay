from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

class BackupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_code')
    hashed_codes = models.TextField(max_length=32, blank=True, null=True)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['hashed_codes', 'user'],
                name='unique_hashed_codes'
            )
        ]  


