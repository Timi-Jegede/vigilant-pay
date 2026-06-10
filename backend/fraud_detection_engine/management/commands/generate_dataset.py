from django.core.management.base import BaseCommand
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate dataset for Data Pre-Processor'

    def handle(self, *args, **options):
        import numpy as np
        import pandas as pd


        np.random.seed(42)
        n_samples = 5000

        data = {
            'transaction_id': [f'TX_{i}' for i in range(n_samples)],
            'user_id': np.random.randint(1000, 9999, n_samples),
            'amount': np.random.exponential(scale=150, size=n_samples) + 5,
            'time_gap_seconds': np.random.choice([np.nan, 12, 45, 600, 86400], size=n_samples, p=[0.05, 0.2, 0.3, 0.3, 0.15]),
            'device_status': np.random.choice(['recognized', 'new device', ''], size=n_samples, p=[0.8, 0.15, 0.05]),
            'isp_name': np.random.choice(['Comcast', 'Verizon', 'Amazon AWS', 'DigitalOcean', 'Unknown Network'], size=n_samples, p=[0.6, 0.25, 0.08, 0.05, 0.02]),
            'historical_fraud_label': np.random.choice([0, 1], size=n_samples, p=[0.96, 0.04])
        }

        df = pd.DataFrame(data)

        df.loc[(df['amount'] > 500) & (df['isp_name'].isin(['Amazon AWS', 'DigitalOcean'])), 'historical_fraud_label'] = 1

        df.to_csv(os.path.join(settings.BASE_DIR, 'data', 'raw_transactions.csv'), index=False)
        self.stdout.write(self.style.SUCCESS(('Success! Generated raw baseline file: "raw_transactions.csv"')))