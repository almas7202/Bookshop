# models.py
from django.db import models
from django.contrib.auth.models import User

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
    averageRating = models.FloatField()
    ratingsCount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book= models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def product_total(self):
        return ((self.book.price)*(self.quantity))
    
    
class CustomerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    add1 = models.CharField(max_length=300)
    add2 = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200,default='India')
    zipcode = models.IntegerField() 
    

    objects = models.Manager()

    def __str__(self):
        return (self.fname +','+ self.add1 +','+ self.add2)
