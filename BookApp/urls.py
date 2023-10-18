from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('base/', views.baseview,name='baseview'),
    path('', views.indexview,name='indexview'),
    path('register/',views.registerview,name='registerview'),
    path('login/',views.loginview,name='loginview'),
    path('shop/',views.shopview,name='shopview'),
    path('cart/',views.cartview,name='cartview'),
    path('booklist/',views.booklistview,name='booklistview'),
    path('checkout/',views.checkoutview,name='checkoutview'),
    path('wishlist/',views.wishlistview,name='wishlistview'),
    path('profile/',views.profileview,name='profileview'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_cart'),
    path('/remove_cart/<int:id>/',views.removecart,name='rem_cart'),
    path('bookdetails/',views.bookdetailsview,name='bookdetails'),


    # path('search/', views.search_books, name='search_books'),
    path('logout/',views.logoutview),





]