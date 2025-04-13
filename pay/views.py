from django.shortcuts import render
from tasks_management.decorators import token_required
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from .settings import SUPPORTED_ACCOUNT_TYPES, DEFAULT_TRANSACTION_PAGE_SIZE

from .models import Account, Transaction
from .converter import convert, SUPPORTED_CURRENCIES
from .transaction_helper import create_transaction
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
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@token_required
def get_account_types(request):
    if request.method == 'GET':
        return JsonResponse({'account_types': SUPPORTED_ACCOUNT_TYPES})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

@token_required
def get_currencies(request):
    if request.method == 'GET':
        return JsonResponse({'currencies': SUPPORTED_CURRENCIES})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@token_required
def open_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        account_number = str(uuid.uuid4()).replace('-', '')[:20]
        account_type = data.get('type')
        balance = 0
        currency = data.get('currency')

        if account_type not in SUPPORTED_ACCOUNT_TYPES:
            return JsonResponse({'message': 'Unsupported account type'}, status=400)

        if currency not in SUPPORTED_CURRENCIES:
            return JsonResponse({'message': 'Unsupported currency'}, status=400)

        if not account_type or not currency:
            return JsonResponse({'message': 'Invalid data'}, status=400)

        account = Account.objects.create(
            account_number=account_number,
            account_type=account_type,
            balance=balance,
            currency=currency,
            owner=request.user
        )
        return JsonResponse({'message': 'Account opened successfully', 'account_number': account.account_number}, status=201)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

@token_required
def deposit(request, account_number):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return JsonResponse({'message': 'Invalid amount. Must be greater than 0.'}, status=400)
        except (InvalidOperation, TypeError):
            return JsonResponse({'message': 'Invalid amount format. Must be a valid decimal number.'}, status=400)

        try:
            account = Account.objects.get(account_number=account_number, owner=request.user)
            account.balance += amount
            account.save()
            create_transaction(
                to_account=account,
                original_amount=amount,
                converted_amount=amount,
                authorized_by=request.user,
                transaction_type='Deposit',
                status='Completed'
            )
            return JsonResponse({'message': 'Deposit successful', 'new_balance': str(account.balance)}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

@token_required
def transfer(request, account_number):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        target_account_number = data.get('target_account')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return JsonResponse({'message': 'Invalid amount. Must be greater than 0.'}, status=400)
        except (InvalidOperation, TypeError):
            return JsonResponse({'message': 'Invalid amount format. Must be a valid decimal number.'}, status=400)

        try:
            source_account = Account.objects.get(account_number=account_number, owner=request.user)
            target_account = Account.objects.get(account_number=target_account_number)

            original_amount = amount
            target_amount = amount
            
            if source_account == target_account:
                create_transaction(
                    to_account=target_account,
                    from_account=source_account,
                    original_amount=original_amount,
                    converted_amount=target_amount,
                    conversion_rate=1,
                    authorized_by=request.user,
                    transaction_type='Transfer',
                    status='Failed (same account)'
                )
                return JsonResponse({'message': 'Cannot transfer to the same account'}, status=400)
            
            coversion_rate = 1
            if source_account.currency != target_account.currency:
                target_amount, coversion_rate = convert(amount, source_account.currency, target_account.currency)

            if source_account.balance < original_amount:
                create_transaction(
                    to_account=target_account,
                    from_account=source_account,
                    original_amount=original_amount,
                    converted_amount=target_amount,
                    conversion_rate=coversion_rate,
                    authorized_by=request.user,
                    transaction_type='Transfer',
                    status='Failed (insufficient funds)'
                )
                return JsonResponse({'message': 'Insufficient funds'}, status=400)

            source_account.balance -= original_amount
            target_account.balance += target_amount

            source_account.save()
            target_account.save()
            create_transaction(
                to_account=target_account,
                from_account=source_account,
                original_amount=original_amount,
                converted_amount=target_amount,
                conversion_rate=coversion_rate,
                authorized_by=request.user,
                transaction_type='Transfer',
                status='Completed'
            )
            return JsonResponse({'message': 'Transfer successful'}, status=200)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account not found'}, status=404)
        except Exception:
            return JsonResponse({'message': 'Transfer failed, try again later'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@token_required
def get_transactions(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', DEFAULT_TRANSACTION_PAGE_SIZE))
        total_pages = Transaction.objects.filter(authorized_by=request.user).count() // page_size + 1
        offset = (page - 1) * page_size
        transactions = Transaction.objects.filter(authorized_by=request.user).order_by('-created_at')[offset:offset + page_size]
        return JsonResponse(
            {
                'transactions': [
                    {
                        'id': t.id,
                        'from_account': t.from_account.account_number if t.from_account else None, 
                        'to_account': t.to_account.account_number, 
                        'original_amount': str(t.original_amount),
                        'original_currency': t.from_account.currency if t.from_account else None,
                        'converted_amount': str(t.converted_amount),
                        'target_currency': t.to_account.currency,
                        'conversion_rate': str(t.conversion_rate), 
                        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
                        'type': t.type, 
                        'status': t.status
                    } for t in transactions
                ],
                'total_pages': total_pages
            }
        )
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)