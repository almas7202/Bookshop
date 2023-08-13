from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('base/', views.baseview,name='baseview'),
    path('', views.indexview,name='indexview'),
    path('register/',views.registerview,name='registerview'),
    path('login/',views.loginview,name='loginview'),
]