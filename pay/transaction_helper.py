from .models import Transaction

def create_transaction(to_account, original_amount, converted_amount, authorized_by, transaction_type, status, from_account=None, conversion_rate=1):
    transaction = Transaction(
        from_account=from_account,
        to_account=to_account,
        original_amount=original_amount,
        converted_amount=converted_amount,
        conversion_rate=conversion_rate,
        authorized_by=authorized_by,
        type=transaction_type,
        status=status
    )
    transaction.save()
    return transaction