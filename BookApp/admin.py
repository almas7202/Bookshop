from django.contrib import admin
from .models import Book,Cart

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'publisher', 'categories', 'maturityRating','imageLinks', 'language', 'Genre', 'averageRating', 'ratingsCount', 'price']

admin.site.register(Book, BookAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ["quantity", "product", "user"][::-1]
admin.site.register(Cart)
