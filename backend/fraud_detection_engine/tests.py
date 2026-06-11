from django.test import TestCase, Client
from unittest.mock import patch
import json

class EvaluateTransactionViewTests(TestCase):
    
    @patch('api_gateway.views.PredictMLModel.predict_transaction_fraud')
    def test_transaction_endpoint(self, mock_predict):
        mock_predict.return_value = 'Safe Transaction'

        payload = {
            "sender": {
                "external_id": 363,
                "device_fingerprint": "fp_xyz123abc789"
            },
            "recipient": {
                "account_number_hash": "a8fbc83d21e8e45"
            },
            "transaction": {
                "transaction_id": 12369,
                "amount": 250.00,
                "current_available_balance": 1200.00
            }
        }

        client = Client()
        response = client.post(
            '/api/evaluate-transaction',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer frd_live_7a3d9f1e_acbe48b29c104ef0bc552d8e391a',
            HTTP_X_FORWARDED_FOR='104.244.42.1'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['prediction'], 'Safe Transaction')

        assert response.status_code == 200
        assert response.json()['prediction'] == 'Safe Transaction'

