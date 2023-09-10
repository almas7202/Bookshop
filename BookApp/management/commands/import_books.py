# myapp/management/commands/import_books.py
import csv
from django.core.management.base import BaseCommand
from BookApp.models import Book  # Import your Book model
from datetime import datetime
class Command(BaseCommand):
    help = 'Import books from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csvfile = options['csvfile']

        with open(csvfile, 'r',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(
                    title=row['title'],
                    authors=row['authors'],
                    publisher=row['publisher'],
                    description=row['description'],
                    categories=row['categories'],
                    maturityRating=row['maturityRating'],
                    imageLinks=row['imageLinks'],
                    language=row['language'],
                    previewLink=row['previewLink'],
                    infoLink=row['infoLink'],
                    Genre=row['Genre'],
                    averageRating=row['averageRating'],
                    ratingsCount = int(float(row['ratingsCount'])),
                    price=row['price']
                )
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {book.title}'))
