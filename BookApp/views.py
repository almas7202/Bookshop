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
from django.http import HttpResponseRedirect


# GOOGLE_BOOKS_API_KEY = 'AIzaSyDqa0wRKCEGjuh9PqBAlqWNvNvxpN-4YNI'
import random


def baseview(request):
    return render(request,'base.html')
    
def generate_random_price():
    return round(random.uniform(350, 850))  # Generates a random price with two decimal places



def indexview(request): 
    query = request.GET.get('q', '')  # Get the search query from the GET request, default to an empty string4


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
        if books:
            recommended_books = get_recommendations(books.first().title, num_recommendations=15)
    print("recommended_books ==============>>>",recommended_books)
    random_book_1 = Book.objects.order_by('?').first()
    # Get the second random book while ensuring it's different from the first one
    random_book_2 = Book.objects.exclude(pk=random_book_1.pk).order_by('?').first()
    random_books = Book.objects.order_by('?')[:10]
    context = {
        'random_books': random_books,
        'random_book_1': random_book_1,
        'random_book_2': random_book_2,
        'query': query,
        # 'genre': genre,
        'books': books,
        'recommended_books': recommended_books
    }
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


# def checkoutview(request):    
#     if request.method == 'POST':
#         form1 = CustomerAddressForm(request.POST)
#         if form1.is_valid():
#             try:
#                 customer = form1.save(commit=False)
#                 customer.user = request.user
#                 customer.save()
#                 return HttpResponseRedirect('/checkout/')  # Redirect to the same page
#             except IntegrityError as e:
#                 print(f"Error saving data: {e}")
#                 messages.error(request, 'There was an error while saving the data')
#         else:
#             # Handle form er
#             # rors
#             errors = form1.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form1 = CustomerAddressForm()

#     selected_address_id = None  # Initialize selected_address_id
#     cart_items = Cart.objects.filter(user=request.user)
#     # Handle address selection
#     if request.method == 'POST' and 'selected_address' in request.POST:
#         selected_address_id = request.POST['selected_address']
#         selected_address = CustomerModel.objects.get(id=selected_address_id)
#         # You can now use `selected_address` in your further processing
#     cust_address = CustomerModel.objects.filter(user=request.user)
#     All_cart = Cart.objects.filter(user=request.user)
#     subtotal = Decimal('0')
#     GST_rate = Decimal('0.05')  # 5% GST rate
#     grandtotal = Decimal('0')
#     subtotal = sum(item.product_total for item in All_cart)
#     GST_amount = subtotal * GST_rate
#     GST_amount=round(GST_amount,2)
#     grand_total = float(subtotal + GST_amount)
#     payment = None  # Initialize payment variable to None   
#     client = razorpay.Client(auth=("rzp_test_7iEeq4gBX0tDwL", "0lj2P8OpvtXavLC2xgOxl43C"))
#     client.set_app_details({"title": "My Django App", "version": "4.1.7"})
#     payment = client.order.create({'amount':(grand_total)*100, 'currency': 'INR','payment_capture': '1'}) 
#     if request.method == 'POST':
#         for cart_item in All_cart:  # Loop through cart items
#             Order.objects.create(
#                 user=request.user,
#                 customer=selected_address,
#                 Book=cart_item.book,  # Use cart_item to access product
#                 quantity=cart_item.quantity
#             )        
#         cart_items.delete()
#         print(cart_items)
#         return redirect('/')
#     context = {
#         'form1': form1,
#         'cust_address': cust_address,
#         'All_cart': All_cart,
#         'subtotal': subtotal,
#         'GST': GST_amount,
#         'payment':payment,
#         'grand_total': grand_total
#     }
#     return render(request, 'shop-checkout.html', context)

def checkoutview(request):
    # Initialize variables
    form1 = CustomerAddressForm()
    selected_address = None
    cust_address = CustomerModel.objects.filter(user=request.user)
    All_cart = Cart.objects.filter(user=request.user)
    subtotal = Decimal('0')
    GST_rate = Decimal('0.05')  # 5% GST rate
    GST_amount = Decimal('0')
    grand_total = Decimal('0')
    payment = None

    if request.method == 'POST':
        # Handle form submission for adding a customer address
        form1 = CustomerAddressForm(request.POST)
        if form1.is_valid():
            try:
                customer = form1.save(commit=False)
                customer.user = request.user
                customer.save()
                return HttpResponseRedirect('/checkout/')
            except IntegrityError as e:
                print(f"Error saving data: {e}")
                messages.error(request, 'There was an error while saving the data')
        else:
            # Handle form errors
            errors = form1.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"{field}: {error}")

    if 'selected_address' in request.POST:
        # Handle address selection
        selected_address_id = request.POST['selected_address']
        try:
            selected_address = CustomerModel.objects.get(id=selected_address_id)
        except CustomerModel.DoesNotExist:
            selected_address = None

    # Calculate the subtotal, GST, and grand total
    for cart_item in All_cart:
        subtotal += cart_item.product_total
    GST_amount = round(subtotal * GST_rate, 2)
    grand_total = subtotal + GST_amount

    if request.method == 'POST':
        # Handle order creation and cart items deletion
        for cart_item in All_cart:
            Order.objects.create(
                user=request.user,
                customer=selected_address,
                Book=cart_item.book,
                quantity=cart_item.quantity
            )
        All_cart.delete()
        return redirect('/order/')

    # Initialize the Razorpay payment
    client = razorpay.Client(auth=("rzp_test_7iEeq4gBX0tDwL", "0lj2P8OpvtXavLC2xgOxl43C"))
    client.set_app_details({"title": "My Book App", "version": "4.1.7"})
    payment = client.order.create({'amount': int(grand_total * 100), 'currency': 'INR', 'payment_capture': '1'})

    context = {
        'form1': form1,
        'cust_address': cust_address,
        'selected_address': selected_address,
        'All_cart': All_cart,
        'subtotal': subtotal,
        'GST': GST_amount,
        'payment': payment,
        'grand_total': grand_total
    }
    return render(request, 'shop-checkout.html', context)



def wishlistview(request):
    return render(request,'wishlist.html')

def profileview(request):
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

def bookdetailsview(request,id):
    get_product=Book.objects.get(id=id)
    context={'get_product':get_product}
    return render(request,'books-detail.html',context)


def orderview(request):
    order_get=Order.objects.filter(user=request.user)
    for i in order_get:
        print(i.Book.title)
    print(order_get)
    context={'order_get':order_get}
    return render(request,'shop-order.html',context)