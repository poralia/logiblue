import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.tracking.models import Country


class Command(BaseCommand):
    help = "Insert bulk countries with CSV file"

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        csv_file = settings.BASE_DIR.parent.parent / 'countries.csv'

        # check file exist
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR('CSV file contries.csv not exist'))
            return

        with open(csv_file) as file:
            reader = csv.reader(file, delimiter=',')
            line_count = 0
            for row in reader:
                Country.objects.update_or_create(
                    iso_code=row[2],
                    defaults={
                        'name': row[0],
                        'flag': row[1],
                        'currency': row[3],
                    }
                )
                line_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Processed {line_count} lines.')
        )
