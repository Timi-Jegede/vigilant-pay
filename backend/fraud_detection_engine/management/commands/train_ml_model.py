from django.core.management.base import BaseCommand
from fraud_detection_engine.ml_model import TrainMLModel

class Command(BaseCommand):
    help = 'Training the Fraud Engine Model using XGBoost'


    def handle(self, *args, **options):
        detector = TrainMLModel()
        detector.train_ml_model()
        self.stdout.write(self.style.SUCCESS('Model training completed!')) 
