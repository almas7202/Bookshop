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
    path('profile/',views.profileview,name='profileview')



]