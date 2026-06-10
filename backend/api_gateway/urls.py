from django.urls import path

from .views import EvaluateTransactionView

app_name = 'api_gateway'

urlpatterns = [
    path('api/evaluate-transaction', EvaluateTransactionView.as_view(), name='evaluate_transaction'),
]