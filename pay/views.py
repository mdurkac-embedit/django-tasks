from django.shortcuts import render
from tasks_management.decorators import token_required
from django.http import JsonResponse
from .models import Account
import json
import uuid

def index(request):
    return render(request, 'index.html')

@token_required
def get_accounts(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return JsonResponse({'accounts': [{'account_number': account.account_number, 'balance': account.balance, 'currency': account.currency, 'account_type': account.account_type} for account in accounts]})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@token_required
def open_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        account_number = str(uuid.uuid4()).replace('-', '')[:20]
        account_type = data.get('type')
        balance = 0
        currency = data.get('currency')

        if not account_type or not currency:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        account = Account.objects.create(
            account_number=account_number,
            account_type=account_type,
            balance=balance,
            currency=currency,
            owner=request.user
        )
        return JsonResponse({'message': 'Account opened successfully', 'account_id': account.id}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
