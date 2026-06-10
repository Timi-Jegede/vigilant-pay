import joblib
from xgboost import XGBClassifier
import numpy as np
from sklearn.metrics import classification_report
from .utils import get_processed_data
import os
from django.conf import settings
import logging
import pandas as pd
from typing import Dict, Any
from django.apps import apps

X_train, X_test, y_train, y_test = get_processed_data('raw_transactions.csv')

logger = logging.getLogger(__name__)

class TrainMLModel:
    def __init__(self):
        self.xgb = None
        self.xgb_predictions = None
        self.output_model_file = ''
    
    def train_ml_model(self):
        print('\n=== Training Model 2: XGBoost ===')
        
        self.xgb = XGBClassifier(n_estimators=100, scale_pos_weight=24, random_state=42)
        self.xgb.fit(X_train, y_train)
        self.xgb_predictions = self.xgb.predict(X_test)
        print(classification_report(y_test, self.xgb_predictions, target_names=['Clean', 'Fraud']))

        
        self.output_model_file = os.path.join(settings.BASE_DIR, 'models', 'production_fraud_model.joblib')
        joblib.dump(self.xgb, self.output_model_file)
        print(f'\n Model artifact generated successfully and saved as: "{self.output_model_file}"')

class PredictMLModel:
    def predict_transaction_fraud(self, features: list):
        try:
            app_config = apps.get_app_config('fraud_detection_engine')
            ml_model = app_config.ml_model
        except LookupError:
            logger.error('Fraud Detection Engine appication layout configuration registry missing.')
            raise RuntimeError('Service temporarily unavailable.')
        
        if ml_model is None:
            logger.error('Inference requested while XGBoost asset is unintialized or null.')
            raise RuntimeError('Model engine asset is unavailable.')
        
        try:
            matrix_input = np.array(features).reshape(1, -1)

            risk_threshold = 0.8

            probabilities = ml_model.predict_proba(matrix_input)
            fraud_probability = float(probabilities[0][1])
            fraud_score = 1.0 if fraud_probability > risk_threshold else 0.0
            
            return {
                'fraud_probability': round(fraud_probability, 2),
                'fraud_score': fraud_score,
                'risk_threshold': risk_threshold
            }
        
        except Exception as e:
            logger.exception(f'Unexpected pipeline execution error during inference: {str(e)}')
            raise RuntimeError(f'Internal engine model inference failure. {str(e)}') 