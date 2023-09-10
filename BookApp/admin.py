from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publisher', 'categories', 'maturityRating','imageLinks', 'language', 'Genre', 'averageRating', 'ratingsCount', 'price')

admin.site.register(Book, BookAdmin)
