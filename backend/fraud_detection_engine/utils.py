import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
from django.conf import settings

class FraudPreprocessingFramework:
    def __init__(self):
        self.amount_mean = 0.0
        self.amount_std = 1.0

    def fit(self, df):
        self.amount_mean = df['amount'].mean()
        self.amount_std = df['amount'].std() if df['amount'].std() > 0 else 1.0
        return self
    
    def transform(self, df):
        processed = pd.DataFrame()

        processed['f1_velocity_ratio'] = 3600 / (df['time_gap_seconds'].fillna(3600) + 1)
        processed['f2_balance_drain_ratio'] = df['amount'] / 5000.0 
        processed['f3_time_gap_seconds'] = df['time_gap_seconds'].fillna(-1)
        processed['f4_mule_indicator'] = np.where(df['amount'] > 2000, 1, 0)
        processed['f5_fanout_ratio'] = np.random.uniform(0.1, 2.5, len(df))
        processed['f6_recipient_historical_risk'] = np.where(df['amount'] > 1500, 0.85, 0.02)

        processed['f7_is_new_device'] = np.where(df['device_status'] == 'new_device', 1, 0) 
        processed['f8_geo_velocity'] = np.where(df['isp_name'].isin(['Amazon AWS', 'DigitalOcean']), 950.0, 45.0)

        isp_map = {
            'Comcast': 0, 'Verizon': 0,
            'Unknown Network': 1,
            'Amazon AWS': 2, 'DigitalOcean': 2
        }

        processed['f9_isp_classification'] = df['isp_name'].map(isp_map).fillna(-1)
        processed['f10_amount_z_score'] = (df['amount'] - self.amount_mean) / self.amount_std
        processed['f11_max_multiplier'] = df['amount'] /(self.amount_mean + 1)

        feature_order = [
            'f1_velocity_ratio', 'f2_balance_drain_ratio', 'f3_time_gap_seconds',
            'f4_mule_indicator', 'f5_fanout_ratio', 'f6_recipient_historical_risk',
            'f7_is_new_device', 'f8_geo_velocity', 'f9_isp_classification',
            'f10_amount_z_score', 'f11_max_multiplier'
        ]

        return processed[feature_order]

def get_processed_data(file='raw_transactions.csv'):
    raw_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'data', file))

    framework = FraudPreprocessingFramework()
    framework.fit(raw_df)
    clean_features = framework.transform(raw_df)
    labels = raw_df['historical_fraud_label']

    return train_test_split(
        clean_features, labels, test_size=0.2, random_state=42, stratify=labels
    )

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = get_processed_data()

    print(f'Pre-pocessing framework successful! Engineered 11 feature rows.')
    print(f'Training Array Size: {X_train.shape}, Verification Test Array Shape: {X_test.shape}')

