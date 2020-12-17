from django.forms import ModelForm
from . import models

class OnlineBalanceForm(ModelForm):
    class Meta:
        model = models.OnlineBalance
        fields = ('amount', 'category')
        labels = {
            "amount": "Сумма",
            "category": "Категория",
            }                

class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        fields = ('name', 'describe')
        labels = {
            "name": "Имя",
            "describe": "Описание",
            }        