from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'publisher', 'categories', 'maturityRating','imageLinks', 'language', 'Genre', 'averageRating', 'ratingsCount', 'price']

admin.site.register(Book, BookAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ["quantity", "product", "user"][::-1]
admin.site.register(Cart)

@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [ "zipcode", "state", "city", "country", "add2", "add1", "mobile", "email", "lname", "fname", "user"][::-1]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "order_date", "quantity", "Book", "customer", "user"]
