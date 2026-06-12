import os
import joblib
import logging
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import sys

logger = logging.getLogger(__name__)

class FraudDetectionEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fraud_detection_engine'
    ml_model = None

    def ready(self):
        is_testing = (
            'test' in sys.argv or 
            'migrate' in sys.argv or 
            'makemigrations' in sys.argv or
            any('pytest' in arg for arg in sys.argv) or
            os.environ.get('SECRET_KEY') == 'ci-test-key'
        )

        if is_testing:
            print('Testing environment detected. Skipping live .joblib model initialization!')
            return

        model_path = os.path.join(settings.BASE_DIR, 'models', 'production_fraud_model.joblib')

        if not os.path.exists(model_path):
            logger.critical(f'Model file missing at runtime: {model_path}')
            raise ImproperlyConfigured(f'Model file missing at: {model_path}')
        
        try:
            loaded_model = joblib.load(model_path)

            if not hasattr(loaded_model, 'predict_proba'):
                raise TypeError('Loaded joblib object is missing "predict_proba" method.')

            FraudDetectionEngineConfig.ml_model = loaded_model
            logger.info('XGBoost fraud detection model successfully loaded into memory.')
        
        except Exception as e:
            logger.exception('Failed to initialize the machine learning model')
            raise ImproperlyConfigured(f'Fatal error loading model pipeline: {str(e)}')
