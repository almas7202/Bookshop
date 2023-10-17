# Trial and Error
from django.shortcuts import render,redirect
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .recommendations import get_recommendations
import json
import requests
import random

from django.db import IntegrityError

# GOOGLE_BOOKS_API_KEY = 'AIzaSyDqa0wRKCEGjuh9PqBAlqWNvNvxpN-4YNI'
import random

def generate_random_price():
    return round(random.uniform(350, 850), 2)  # Generates a random price with two decimal places


def baseview(request):
    return render(request,'base.html')
    
def generate_random_price():
    return round(random.uniform(350, 850))  # Generates a random price with two decimal places

def search_books(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request, default to an empty string

    # Perform a case-insensitive search across multiple fields
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(authors__icontains=query) |
        Q(description__icontains=query)
    )

    # Apply order_by to the queryset before slicing
    books = books.order_by('title')[:20]

    recommended_books = []  # Initialize an empty list for recommendations

    if query:
        # If a query is provided, get recommendations for the first book in the search results
        if books:
            recommended_books = get_recommendations(books.first().title, num_recommendations=15)

    return render(request, 'index.html', {'query': query, 'books': books, 'recommended_books': recommended_books})


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

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You are Successfully Logged Out !')
    return redirect('/login/')
    
def shopview(request):
    book_list = Book.objects.all()  # Get all books from the databas
    paginator = Paginator(book_list, 52)  # Create a Paginator object with 50 books per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the Page object for the requested page
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'books-grid-view.html', context)

from decimal import Decimal

def cartview(request):
    if request.user.is_authenticated:
        All_cart = Cart.objects.filter(user=request.user)
        cart_count = Cart.objects.filter(user=request.user).count()
        subtotal = Decimal('0')
        GST_rate = Decimal('0.05')  # 5% GST rate
        grandtotal = Decimal('0')
        if request.method == 'POST':
            form = UpdateCartQuantityForm(request.POST)
            if form.is_valid():
                # Get the product and updated quantity from the form
                product_id = form.cleaned_data['product_id']
                updated_quantity = form.cleaned_data['quantity']

                # Update the cart item with the new quantity
                cart_item = Cart.objects.get(user=request.user, book_id=product_id)
                cart_item.quantity = updated_quantity
                cart_item.save()

        for item in All_cart:
            # Calculate the GST for each item and add it to the subtotal
            item.subtotal_with_GST = item.product_total * (Decimal('1') + GST_rate)
            subtotal += item.subtotal_with_GST

        subtotal=round(subtotal)
        # Calculate GST amount for the entire cart
        GST_amount = round(subtotal - (subtotal / (Decimal('1') + GST_rate)))

        # Calculate grand total including GST and shipping
        grandtotal = round(subtotal +GST_amount)

        context = {
            'cart_data': All_cart,
            'count': cart_count,
            'subtotal': subtotal,
            'GST': GST_amount,
            'grandtotal': grandtotal
        }

        return render(request, 'shop-cart.html', context)
    else:
        return redirect('/login/')

def removecart(request, id):
    get_product = Cart.objects.get(user=request.user, id=id)
    get_product.delete()
    return redirect('/cart/')



def booklistview(request):
    return render(request,'books-list.html')


def checkoutview(request):    
    cust_address = CustomerModel.objects.filter(user=request.user)
    All_cart = Cart.objects.filter(user=request.user)
    subtotal = Decimal('0')
    GST_rate = Decimal('0.05')  # 5% GST rate
    grandtotal = Decimal('0')
    for item in All_cart:
        # Calculate the GST for each item and add it to the subtotal
        item.subtotal_with_GST = item.product_total * (Decimal('1') + GST_rate)
        subtotal += item.subtotal_with_GST
    subtotal=round(subtotal)
    # Calculate GST amount for the entire cart
    GST_amount = round(subtotal - (subtotal / (Decimal('1') + GST_rate)))

    # Calculate grand total including GST and shipping
    grandtotal = round(subtotal +GST_amount)
    if request.method == 'POST':
        form1 = CustomerAddressForm(request.POST)
        if form1.is_valid():
            try:
                print(request.user)
                customer = form1.save(commit=False)
                customer.user = request.user
                customer.save()
                return redirect('/checkout/')
            except IntegrityError as e:
                print(f"Error saving data: {e}")
                messages.error(request, 'There was an error while saving the data.')
        else:
            errors = form1.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form1 = CustomerAddressForm()
    context={'form1': form1,'cust_address':cust_address,'All_cart':All_cart,'subtotal': subtotal,'GST': GST_amount,'grandtotal': grandtotal}    
    return render(request, 'shop-checkout.html',context)
    

def wishlistview(request):
    return render(request,'wishlist.html')

def profileview(request):

    return render(request,'my-profile.html')
    return render(request,'my-profile.html')
    


# from .models import ShoppingCartItem

def add_to_cart(request, id):
    if request.user.is_authenticated:
        user=request.user
        cart_items=Cart.objects.filter(user=request.user)
        get_product=Book.objects.get(id=id)
        is_in=Cart.objects.filter(
            user=request.user,
            book=get_product
        ).exists()
        if is_in:
            for i in cart_items:
                i.quantity += 1
                i.save()
        else:
            Cart(
                user=request.user,
                book=get_product
            ).save()
    else:
        messages.error(request, 'Please Login First to add item in cart !!!')
        return redirect('/login/')
    return redirect('/cart/')

def view_cart(request):
    cart_items = ShoppingCartItem.objects.filter(user=request.user)
    total_price = sum(item.price * item.quantity for item in cart_items)
    context={'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart_view.html',context )

def AddressView(request):
    pass