from django.shortcuts import render,redirect
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import random


# GOOGLE_BOOKS_API_KEY = 'AIzaSyDqa0wRKCEGjuh9PqBAlqWNvNvxpN-4YNI'



def baseview(request):
    return render(request,'base.html')


def indexview(request): 
    google_books_api_key = 'AIzaSyBOgiz9kM8HnX1vtgT8106HgGSOUQ2e7Y4'
    url = f'https://www.googleapis.com/books/v1/volumes?q=Harry+Potter&key={google_books_api_key}&maxResults=10'
    
    response = requests.get(url)
    data = response.json()

    # Extract the list of books from the API response
    books = data.get('items', [])


    categories = ['comedy', 'adventure', 'thriller']
    random_category = random.choice(categories)  # Select a random category

    # Construct the API URL with the selected category
    url1 = f'https://www.googleapis.com/books/v1/volumes?q=subject:{random_category}&key={google_books_api_key}&maxResults=10'

    response = requests.get(url1)
    data = response.json()

    # Extract the list of books from the API response
    r_books = data.get('items', [])

    context = {'books': books,'r_books':r_books}

    return render(request,'index.html',context)

def registerview(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = RegistrationForm()   
    return render(request,'registration.html',{'form':form})


def loginview(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user)
            return redirect('/')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'login.html')

def shopview(request):
    return render(request,'books-grid-view.html')

def cartview(request):
    return render(request,'shop-cart.html')

def booklistview(request):
    return render(request,'books-list.html')

def checkoutview(request):
    return render(request,'shop-checkout.html')

def wishlistview(request):
    return render(request,'wishlist.html')

def profileview(request):
    return render(request,'my-profile.html')
    




 #commment BY   