from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from fraud_detection_engine.services.features_service import MLFeatureService
from fraud_detection_engine.ml_model import PredictMLModel
from .serializers import TransactionSerializer


User = get_user_model()

# Create your views here.

class EvaluateTransactionView(APIView):
    def post(self, request):
        native_req = request._request
        
        payload = getattr(native_req, 'json_payload', {})
        platform = getattr(native_req, 'auth_platform', {})

        ip_intelligence = getattr(native_req, 'ip_intelligence', {})
        current_lat = ip_intelligence.get('latitude', 0.0)
        current_lon = ip_intelligence.get('longtitude', 0.0)
        f9_isp_classification = ip_intelligence.get('f9_isp_classification')

        serializer = TransactionSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        clean_payload = serializer.validated_data

        features = MLFeatureService().extract_all_ml_features(clean_payload, platform, current_lat, current_lon, f9_isp_classification)

        ml_model = PredictMLModel()
        transaction_evaluation = ml_model.predict_transaction_fraud(features)
        fraud_probability = transaction_evaluation['fraud_probability']
        fraud_score = transaction_evaluation['fraud_score']
        risk_threshold = transaction_evaluation['risk_threshold']

        return JsonResponse({
            'fraud_probability': fraud_probability,
            'fraud_score': fraud_score,
            'action': 'BLOCK' if fraud_probability > risk_threshold else 'APPROVE'
        })
