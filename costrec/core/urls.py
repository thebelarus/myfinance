from django.urls import path, include
from . import views
urlpatterns = [
    path('get/categories/', views.get_category, name='get_category'),
    path('get/balance/', views.get_balance, name='get_balance'),    
    path('get/currency/', views.get_currency, name='get_currency'),
    path('get/account/', views.get_account, name='get_account'),
    path('add/categories/', views.add_category, name='add_category'),
    path('add/balance/', views.add_balance, name='add_balance'),
    path('add/currency/', views.add_currency, name='add_currency'),
    path('add/account/', views.add_account, name='add_account'),
]