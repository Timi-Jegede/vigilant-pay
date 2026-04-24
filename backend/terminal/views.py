from django.shortcuts import render
import pandas as pd
from dashboard.utils import get_data_path
from django.http import JsonResponse
from users.models import Transaction
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

# Create your views here.

def endpoint(request):
    return render(request, 'terminal/endpoint.html')

@login_required
def card_terminal(request):
    return render(request, 'terminal/card-terminal.html')

def countries_json(request):
    countries = get_data_path('countries.csv')
    df = pd.read_csv(countries, encoding='latin1')
    df.columns = df.columns.str.lower()
    countries_json = df.to_json(orient='records', indent=4)

    return JsonResponse({'countries': countries_json})

@login_required
def save_transaction(request):
    try:
        if request.method == 'POST':
            cardholder_name = request.POST.get('cardholder-name')
            card_number = request.POST.get('card-number')
            expiry_date = request.POST.get('expiry-date')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            location = request.POST.get('location')
            merchant_type = request.POST.get('merchant-type')
            ip_address = request.POST.get('ip-address')
            transaction_date = request.POST.get('transaction-date')
           
            transaction_obj = Transaction(user=request.user)
            transaction_saved = transaction_obj.save_user_transaction(
                            cardholder_name, card_number, expiry_date, 
                            amount, currency, location, merchant_type, ip_address, 
                            transaction_date
                        )

            return render(request, 'terminal/card-terminal.html', {'transaction_saved': transaction_saved})
        return render(request, 'terminal/card-terminal.html')
        
    except Exception as e:
        return render(request, 'terminal/card-terminal.html', {'error': f'An error occurred {e}'})
    


        