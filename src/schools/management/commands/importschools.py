from django.core.management.base import BaseCommand
from schools.utils import import_schools_from_csv

class Command(BaseCommand):
    help = "Import schools from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        result = import_schools_from_csv(csv_file)
        self.stdout.write(self.style.SUCCESS(result))