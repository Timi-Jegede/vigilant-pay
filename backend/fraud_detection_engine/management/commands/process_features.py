import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.model_selection import train_test_split
from dashboard.utils import get_data_path
from django.conf import settings
import os

from fraud_detection_engine.utils import FraudPreprocessingFramework

class Command(BaseCommand):
    help = 'Runs the preprocessor framework and outputs the engineered marix splits shape.'

    def handle(self, *args, **options):
        self.stdout.write('Loading raw transaction data...')

        try:
            raw_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'data', 'raw_transactions.csv'))
        except FileNotFoundError:
            self.stderr.write(
                'Error: "raw_transactions.csv" file not found in your root directory.'
            )
            return
        
        framework = FraudPreprocessingFramework()
        framework.fit(raw_df)

        clean_features = framework.transform(raw_df)
        labels = raw_df['historical_fraud_label']

        X_train, X_test, y_train, y_test = train_test_split(
            clean_features, labels, test_size=0.2, random_state=42, stratify=labels
        )

        self.stdout.write(self.style.SUCCESS('Successfully ran the pre-processing framework!'))
        
        self.stdout.write(f'-> X_train shape (Rows, Columns): {X_train.shape}')
        self.stdout.write(f'-> X_test shape (Rows, Columns): {X_test.shape}')