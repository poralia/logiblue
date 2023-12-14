import csv
import os

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from apps.tracking.models import Category, Country


class Command(BaseCommand):
    help = "Insert bulk categories with CSV file"

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        csv_file = settings.BASE_DIR.parent.parent / 'categories.csv'

        # check file exist
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR('CSV file categories.csv not exist'))
            return

        with open(csv_file) as file:
            reader = csv.reader(file, delimiter=',')
            line_count = 0
            for row in reader:
                try:
                    country = Country.objects.get(iso_code=row[0])
                    Category.objects.update_or_create(
                        title=row[1],
                        country=country,
                        defaults={
                            'price_per_kilo': row[2],
                        }
                    )
                    line_count += 1
                except ObjectDoesNotExist:
                    pass

        self.stdout.write(
            self.style.SUCCESS(f'Processed {line_count} lines.')
        )
