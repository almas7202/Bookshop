from django.shortcuts import render,redirect
from .form import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def baseview(request):
    return render(request,'base.html')


def indexview(request):
    return render(request,'index.html')

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
    if request.method == 'POST': #this is post Request
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