import csv
from django.core.management.base import BaseCommand
from BookApp.models import Book  # Import your Book model from your Django app

class Command(BaseCommand):
    help = 'Load data from a CSV file into the Book model'

    def handle(self, *args, **kwargs):
        csv_file_path = 'F:\BookProject\Books_data_final.csv'  # Predefined path to your CSV file
        self.load_data_from_csv(csv_file_path)

    def load_data_from_csv(self, csv_file_path):
        # Specify the character encoding (e.g., 'utf-8' or 'ISO-8859-1')
        encoding = 'utf-8'  # Adjust this based on the actual encoding of your CSV file

        with open(csv_file_path, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book.objects.create(
                    title=row['title'],
                    authors=row['authors'],
                    # Add other fields here
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {book.title}'))
