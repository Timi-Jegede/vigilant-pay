from django.test import TestCase, Client, override_settings
from types import SimpleNamespace
from unittest.mock import patch
import json

class EvaluateTransactionViewTests(TestCase):
    
    @patch('api_gateway.views.PredictMLModel')
    @patch('fraud_detection_engine.services.features_service.MLFeatureService.extract_all_ml_features')
    @override_settings(MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fraud_detection_engine.middleware.FraudDataEnrichmentMiddleware',
    ])
    def test_transaction_endpoint(self, mock_extract_features, mock_model_class):
        mock_instance = mock_model_class.return_value
        mock_instance.predict_transaction_fraud.return_value = {
            'fraud_probability': 0.15,
            'fraud_score': 15,
            'risk_threshold': 0.50
        }

        mock_extract_features.return_value = ['dummy_feature_1', 'dummy_feature_2']

        payload = {
            "sender": {
                "external_id": 363,
                "device_fingerprint": "fp_xyz123abc789"
            },
            "recipient": {
                "account_number_hash": "a8fbc83d21e8e45"
            },
            "transaction": {
                "transaction_id": 12349,
                "amount": 250.00,
                "current_available_balance": 1200.00
            }
        }

        client = Client()

        mock_ip_intelligence = {
            'latitude': 6.5244, 
            'longitude': 3.3792,
            'f9_isp_classification': 'residential'
        }

        mock_platform_object = SimpleNamespace(id=99, name='test_platform')

        with patch('django.core.handlers.wsgi.WSGIRequest.json_payload', payload, create=True), \
                patch('django.core.handlers.wsgi.WSGIRequest.auth_platform', mock_platform_object, create=True), \
                patch('django.core.handlers.wsgi.WSGIRequest.ip_intelligence', mock_ip_intelligence, create=True):
                client.raise_request_exception = True

                response = client.post(
                    '/api-gateway/api/evaluate-transaction',
                    data=json.dumps(payload),
                    content_type='application/json',
                    HTTP_AUTHORIZATION='Bearer frd_live_7a3d9f1e_acbe48b29c104ef0bc552d8e391a',
                    HTTP_X_FORWARDED_FOR='104.244.42.1'
                )

        if response.status_code == 500:
            print('\n BACKEND CRASH DATA RESPONSE TEXT:', response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['action'], 'APPROVE')
        self.assertEqual(response_data['fraud_score'], 15)
        self.assertEqual(response_data['fraud_probability'], 0.15)

