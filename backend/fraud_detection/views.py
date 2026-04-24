from django.shortcuts import render, redirect
from django.http import JsonResponse
from .mongo_service import MongoService
from django.views.decorators.csrf import csrf_exempt
from .ml_model import FraudDetector
import json
from datetime import datetime
from django.views.decorators.http import require_http_methods
from .alert_service import EmailService
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def index(request):
    return render(request, 'fraud_detection/index.html')

@csrf_exempt
@require_http_methods(['POST'])
def predict_fraud(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = float(data.get('amount', 0))
        merchant = data.get('merchant', '')

        hour = datetime.now().hour
        merchant_risk = calculate_merchant_risk(merchant)

        detector = FraudDetector()
        prediction = detector.predict(amount, hour, merchant_risk)

        fraud_prob = float(prediction['probability'])
        confidence_score = float(prediction['confidence_score'])
        shap_values = prediction['shap_values']

        is_fraud = fraud_prob > 0.5

        mongo = MongoService()
        transaction_id = mongo.save_transaction(amount, merchant, fraud_prob, is_fraud)

        if is_fraud:
            mongo.enqueue(
                transaction_id=transaction_id,
                status='pending',
                reason_for_flagging='High Probability Fraud',
                shap_values=shap_values,
                model_confidence_score=confidence_score,
            )

            email = EmailService()
            email.send_fraud_alert('timmix000@gmail.com', {
                'amount': amount,
                'merchant': merchant,
                'risk_score': fraud_prob
            })

        return JsonResponse({
            'fraud_probability': round(fraud_prob, 3),
            'is_fraud': is_fraud,
            'risk_level': 'HIGH' if fraud_prob > 0.5 else 'MEDIUM' if fraud_prob > 0.2 else 'LOW'
        })
    
    return JsonResponse({'error': 'POST required'}, status=405)

def stats(request):
    mongo = MongoService()
    stats = mongo.get_fraud_stats()
    return JsonResponse(stats)

def calculate_merchant_risk(merchant):
    merchant_lower = merchant.lower()
    high_risk = ['suspicious store', 'unknown merchant', 'cash advance', 'foreign atm']
    medium_risk = ['online_store', 'electronics', 'hotel', 'car rental']

    if merchant_lower in high_risk:
        return 0.85
    elif merchant_lower in medium_risk:
        return 0.5
    else:
        return 0.15

def signup(request):
    return render(request, 'fraud_detection/signup.html')

@require_http_methods(['POST'])
def register_users(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm-password')

    if password == confirm_password:
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.save()
        
        return redirect('/')


        




