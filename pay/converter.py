from django.utils import timezone
from .models import ConversionTable
import requests
from decimal import Decimal, ROUND_HALF_UP
from .settings import SUPPORTED_CURRENCIES, TIME_TO_REFRESH

def convert(amount, from_currency, to_currency):
    try:
        cutoff_time = timezone.now() - timezone.timedelta(seconds=TIME_TO_REFRESH)
        rate = ConversionTable.objects.get(base_currency=from_currency, target_currency=to_currency, updated_at__gte=cutoff_time)
        print(f'Conversion rate found in DB: {rate.conversion_rate}')
    except ConversionTable.DoesNotExist:
        update_converion_rates(from_currency)
        try:
            rate = ConversionTable.objects.get(base_currency=from_currency, target_currency=to_currency, updated_at__gte=cutoff_time)
            print(f'Conversion rate found in DB after update: {rate.conversion_rate}')
        except ConversionTable.DoesNotExist:
            raise Exception("Conversion rate not found. Please update conversion rates.")
    converted_amount = Decimal(amount) * rate.conversion_rate
    return converted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), rate.conversion_rate

def update_converion_rates(from_currency):
    response = requests.get(f"https://open.er-api.com/v6/latest/{from_currency}")
    if response.status_code == 200:
        data = response.json()
        conversion_rates = data.get('rates', {})
        for currency, rate in conversion_rates.items():
            if currency in SUPPORTED_CURRENCIES and currency != from_currency:
                print(f'Updating conversion rate from {from_currency} to {currency}: {rate}')
                new_rate = ConversionTable.objects.filter(
                    base_currency=from_currency,
                    target_currency=currency
                ).first()
                if not new_rate:
                    new_rate = ConversionTable(base_currency=from_currency, target_currency=currency)
                new_rate.conversion_rate = Decimal(rate)
                new_rate.updated_at = timezone.now()
                new_rate.save()
    else:
        raise Exception("Failed to fetch conversion rates")