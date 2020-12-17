from django.urls import path, include
from . import views
urlpatterns = [
    path('get/categories/', views.categories, name='get_categories'),
    path('get/balance/', views.online_balance, name='get_online_balance'),
]