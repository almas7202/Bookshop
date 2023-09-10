from django.shortcuts import render,redirect
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator

import requests
import random


# GOOGLE_BOOKS_API_KEY = 'AIzaSyDqa0wRKCEGjuh9PqBAlqWNvNvxpN-4YNI'
import random

def generate_random_price():
    return round(random.uniform(350, 850), 2)  # Generates a random price with two decimal places



def baseview(request):
    return render(request,'base.html')


def generate_random_price():
    return round(random.uniform(350, 850))  # Generates a random price with two decimal places

def indexview(request): 
    google_books_api_key = 'AIzaSyBOgiz9kM8HnX1vtgT8106HgGSOUQ2e7Y4'
      # Replace with your Google Books API key
    url = f'https://www.googleapis.com/books/v1/volumes?q=Harry+Potter&key={google_books_api_key}&maxResults=10'
    
    response = requests.get(url)
    data = response.json()

    # Extract the list of books from the API response
    books = data.get('items', [])

    # Add random prices to the fetched books
    for book in books:
        book['price'] = generate_random_price()

    categories = ['comedy', 'adventure', 'thriller']
    random_category = random.choice(categories)  # Select a random category

    # Construct the API URL with the selected category
    url1 = f'https://www.googleapis.com/books/v1/volumes?q=subject:{random_category}&key={google_books_api_key}&maxResults=10'

    response = requests.get(url1)
    data = response.json()

    # Extract the list of books from the API response
    r_books = data.get('items', [])

    # Add random prices to the fetched random category books
    for r_book in r_books:
        r_book['price'] = generate_random_price()

    context = {'books': books, 'r_books': r_books}

    return render(request, 'index.html', context)



# def indexview(request): 
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




    google_books_api_key = 'AIzaSyBOgiz9kM8HnX1vtgT8106HgGSOUQ2e7Y4'  # Replace with your Google Books API key
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject&maxResults=50&key={google_books_api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        if 'items' in data:
            categories = set()

            for item in data['items']:
                if 'categories' in item['volumeInfo']:
                    categories.update(item['volumeInfo']['categories'])
            return render(request, 'categories.html', {'categories': list(categories)})
        else:
            return render(request, 'categories.html', {'categories': []})
    except Exception as e:
        print(f"Error fetching categories: {str(e)}")

        return render(request, 'books-grid-view.html', {'categories': []})

def shopview(request):
    google_books_api_key = 'AIzaSyBOgiz9kM8HnX1vtgT8106HgGSOUQ2e7Y4'

    categories = ['Mystery', 'Horror', 'Fairytale', 'Satire', 'Poetry']  # Replace with actual categories

    books = []

    for category in categories:
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{category}&maxResults=12&key={google_books_api_key}'

        try:
            response = requests.get(url)
            data = response.json()

            if 'items' in data:
                for item in data['items']:
                    book = item['volumeInfo']
                    book['category'] = category
                    book['price'] = round(random.uniform(350, 870))  # Random price between $350 and $870


                    if 'imageLinks' in book:
                        # Extract the thumbnail image link
                        thumbnail_link = book['imageLinks'].get('thumbnail')
                        book['thumbnail_link'] = thumbnail_link
                    books.append(book)

            print(books)

        except Exception as e:
            print(f"Error fetching books: {str(e)}")

    # Create a Paginator instance with 12 books per page
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')  # Get the current page number from the request

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    context = {'page': page}

    return render(request, 'books-grid-view.html', context)


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
    


# from .models import ShoppingCartItem

def add_to_cart(request, isbn_id):
    # Get the book details from your database or API
    book = ShoppingCartItem.objects.get(pk=isbn_id)

    # Create or update a shopping cart item for the user
    cart_item, created = ShoppingCartItem.objects.get_or_create(
        user=request.user,
        isbn=isbn,
        book_title=book.title,
        price=book.price,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/shop/')

def view_cart(request):
    cart_items = ShoppingCartItem.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    context={'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart_view.html',context )

