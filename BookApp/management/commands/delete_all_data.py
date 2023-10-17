from django.core.management.base import BaseCommand
from BookApp.models import Book 

class Command(BaseCommand):
    help = 'Deletes all data from the specified model'

    def add_arguments(self, parser):
        parser.add_argument('Book', type=str, help='Name of the model to delete data from')

    def handle(self, *args, **options):
        model_name = options['Book']

        # Check if the model exists
        if model_name not in Book.__name__:
            self.stdout.write(self.style.ERROR(f'Model {Book} does not exist.'))
            return

        # Delete all data from the specified model
        Book.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'All data from {Book} has been deleted.'))
