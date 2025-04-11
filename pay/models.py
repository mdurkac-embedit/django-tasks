from django.db import models
from tasks_management.models import User

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
    
class ConversionTable(models.Model):
    base_currency = models.CharField(max_length=10)
    target_currency = models.CharField(max_length=10)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('base_currency', 'target_currency')

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency} - {self.conversion_rate}"
    
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_transactions', null=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_transactions')
    original_amount = models.DecimalField(max_digits=10, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    authorized_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)