from django.urls import path, include
from . import views
urlpatterns = [
    path('get/categories/', views.get_category, name='get_categories'),
    path('get/balance/', views.get_balance, name='get_balance'),    
    path('add/categories/', views.add_category, name='add_categories'),
    path('add/balance/', views.add_balance, name='add_balance'),
]