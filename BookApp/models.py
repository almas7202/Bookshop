# models.py
from django.db import models
from django.contrib.auth.models import User

import json

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.CharField(max_length=255)
    maturityRating = models.CharField(max_length=255)
    imageLinks = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    previewLink = models.CharField(max_length=255)
    infoLink = models.CharField(max_length=255)
    Genre = models.CharField(max_length=255)
    averageRating = models.FloatField(null=True, blank=True)  # Allow null values
    ratingsCount = models.IntegerField(null=True, blank=True)  # Allow null values
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Provide a default value

    @property
    def thumbnail(self):
        thumbnail_data = json.loads(self.imageLinks.replace("'", "\"")) if self.imageLinks != '' else ''
        return thumbnail_data['smallThumbnail'] if isinstance(thumbnail_data, dict) else ''
        
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book= models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def product_total(self):
        return ((self.book.price)*(self.quantity))
    
    
