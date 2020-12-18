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


class CurrencyForm(ModelForm):
    class Meta:
        model = models.Currency
        fields = ('name', 'currency_code','code')
        verbose_name = 'Валюта'   
        verbose_name_plural = 'Валюты'              
        labels = {
            "name": "Название валюты",
            "currency_code": "Международный код валюты",
            "code":"Cимвол валюты"
            }           

class AccountForm(ModelForm):
    class Meta:
        model = models.Account
        fields = ('name', 'currency','amount')
        verbose_name = 'Счет'   
        verbose_name_plural = 'Счета'    
        labels = {
            "name": "Имя счета",
            "currency": "Валюта",
            "datetime":"Дата добавления",
            "amount":"Баланс"
            }   
    