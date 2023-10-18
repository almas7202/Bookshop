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
import razorpay
from django.db import IntegrityError

# GOOGLE_BOOKS_API_KEY = 'AIzaSyDqa0wRKCEGjuh9PqBAlqWNvNvxpN-4YNI'
import random

def generate_random_price():
    return round(random.uniform(350, 850), 2)  # Generates a random price with two decimal places


def baseview(request):
    return render(request,'base.html')
    
def generate_random_price():
    return round(random.uniform(350, 850))  # Generates a random price with two decimal places



def indexview(request): 
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
    print(recommended_books)
    random_book_1 = Book.objects.order_by('?').first()
    # Get the second random book while ensuring it's different from the first one
    random_book_2 = Book.objects.exclude(pk=random_book_1.pk).order_by('?').first()
    random_books = Book.objects.order_by('?')[:10]
    context={'random_books':random_books, 'random_book_1': random_book_1,
            'random_book_2': random_book_2,'query': query, 'books': books, 'recommended_books': recommended_books}    
    return render(request, 'index.html', context)

    
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
            login(request, user)
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
        subtotal = sum(item.product_total for item in All_cart)

        #  Define your GST rate as a Decimal (e.g., 0.18 for 18% GST)
        GST_rate = Decimal('0.05')

        # Calculate the GST amount for the entire cart
        GST_amount = subtotal * GST_rate
        GST_amount=round(GST_amount,2)

        # Calculate the grand total by adding the subtotal and GST amount
        grand_total = subtotal + GST_amount
        
        context = {
            'cart_data': All_cart,
            'count': cart_count,
            'subtotal': subtotal,
            'GST': GST_amount,
            'grand_total': grand_total
        }

        return render(request, 'shop-cart.html', context)
    else:
        return redirect('/login/')

def removecart(request, id):
    get_product = Cart.objects.get(user=request.user, id=id)
    get_product.delete()
    return redirect('/cart/')



def booklistview(request):
    book_list=Book.objects.all()
    paginator = Paginator(book_list, 52)  # Create a Paginator object with 50 books per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the Page object for the requested page
    context = {
        'page_obj': page_obj,
    }
    return render(request,'books-list.html',context)


def checkoutview(request):    
    if request.method == 'POST':
        form1 = CustomerAddressForm(request.POST)
        if form1.is_valid():
            try:
                customer = form1.save(commit=False)
                customer.user = request.user
                customer.save()
                return HttpResponseRedirect('/checkout/')  # Redirect to the same page
            except IntegrityError as e:
                print(f"Error saving data: {e}")
                messages.error(request, 'There was an error while saving the data')
        else:
            # Handle form er
            # rors
            errors = form1.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form1 = CustomerAddressForm()

    selected_address_id = None  # Initialize selected_address_id
    cart_items = Cart.objects.filter(user=request.user)
    # Handle address selection
    if request.method == 'POST' and 'selected_address' in request.POST:
        selected_address_id = request.POST['selected_address']
        selected_address = CustomerModel.objects.get(id=selected_address_id)
        # You can now use `selected_address` in your further processing

    cust_address = CustomerModel.objects.filter(user=request.user)
    All_cart = Cart.objects.filter(user=request.user)
    
    subtotal = Decimal('0')
    GST_rate = Decimal('0.05')  # 5% GST rate
    grandtotal = Decimal('0')

    for item in All_cart:
        # Calculate the GST for each item and add it to the subtotal
        item.subtotal_with_GST = item.product_total * (Decimal('1') + GST_rate)
        subtotal += item.subtotal_with_GST
    subtotal = round(subtotal)
    # Calculate GST amount for the entire cart
    GST_amount = round(subtotal - (subtotal / (Decimal('1') + GST_rate)))

    # Calculate grand total including GST and shipping
    grandtotal = round(subtotal + GST_amount)
    client = razorpay.Client(auth=("rzp_test_7iEeq4gBX0tDwL", "0lj2P8OpvtXavLC2xgOxl43C"))
    payment = client.order.create({'amount':(grandtotal)*100, 'currency': 'INR','payment_capture': '1'})
    if request.method == 'POST':
        Order(user=request.user,customer=selected_address,Book=(item.book),quantity=(item.quantity)).save()  
        cart_items.delete()
        return redirect('/')


    context = {
        'form1': form1,
        'cust_address': cust_address,
        'All_cart': All_cart,
        'subtotal': subtotal,
        'GST': GST_amount,
        'payment':payment,
        'grandtotal': grandtotal
    }

    return render(request, 'shop-checkout.html', context)


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

def bookdetailsview(request):
    return render(request,'books-detail.html')