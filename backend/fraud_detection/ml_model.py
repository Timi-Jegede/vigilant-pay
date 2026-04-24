import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings
from .data_generator import generate_fraud_dataset
import shap

class FraudDetector:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model_path = os.path.join(settings.BASE_DIR, 'fraud_model.pkl')
    
    def train(self, num_samples=5000):
        df = generate_fraud_dataset(num_samples)

        X = df[['amount_normalized', 'hour_normalized', 'merchant_risk']].values
        y = df['is_fraud'].values

        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)

        print(f'Model trained on {len(df)} samples')
        print(f'Fraud rate: {y.mean():.2%}')

    def predict(self, amount, hour, merchant_risk):
        if not os.path.exists(self.model_path):
            self.train()
        else:
            self.model = joblib.load(self.model_path)

        features = np.array([[amount/1000, hour/24, merchant_risk]])
        probability = self.model.predict_proba(features)[0][1]
        confidence_score = np.max(self.model.predict_proba(features)[0])

        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(features)
        rounded = np.round(shap_values, 3)
        fraud_values = rounded[0][:, 1]
        mapped = dict(zip(['amount', 'hour', 'merchant_risk'], fraud_values.tolist()))
        return {'probability': probability, 'confidence_score': confidence_score, 'shap_values': mapped}
