from django.db import models
from tasks_management.models import User
# Create your models here.

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

    def __str__(self):
        return f"{self.account_type} - {self.account_number}"