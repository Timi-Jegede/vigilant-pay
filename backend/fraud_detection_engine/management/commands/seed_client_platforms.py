import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from fraud_detection_engine.models import ClientPlatform

class Command(BaseCommand):
    help='Seeds the PostgreSQL database from raw transactions CSV file'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'client_platforms.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File missing at: {csv_file_path}'))
            return
        
        self.stdout.write(self.style.NOTICE('Initializing database seed...'))

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            with transaction.atomic():
                success_count = 0

                for row in reader:
                    try:
                        csv_company_name = row['company_name']
                        csv_api_key = row['api_key']
                        csv_is_active = row['is_active']

                        _, created = ClientPlatform.objects.get_or_create(
                            company_name = csv_company_name,
                            api_key = csv_api_key,
                            is_active = csv_is_active
                        )

                        if created:
                            success_count += 1

                    except Exception as row_error:
                        self.stdout.write(self.style.WARNING(f'Skipping corrupt row: {row_error}'))
                        continue
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {success_count} platform entrie(s) into PostgreSQL!'))