from django.forms import ModelForm
from . import models
from django import forms

# class OnlineBalanceForm(ModelForm):
#     class Meta:
#         model = models.OnlineBalance
#         fields = ('amount', 'category')
#         labels = {
#             "amount": "Сумма",
#             "category": "Категория",
#             }                

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
            "amount":"Начальный баланс"
            }   
    
class IncomeCategoryForm(ModelForm):
    class Meta:
        model = models.IncomeCategory
        fields = ('name',)
        labels = {
            "name": "Имя",
            }        

class ExpensesCategoryForm(ModelForm):
    class Meta:
        model = models.ExpensesCategory
        fields = ('name',)
        labels = {
            "name": "Имя",
            }        
        
class IncomeSubCategoryForm(ModelForm):
    class Meta:
        model = models.IncomeSubCategory
        fields = ('name', 'describe', 'parent')
        labels = {
            "name": "Имя",
            "describe": "Описание",
            "parent":"Категория"
            }  


class ExpensesSubCategoryForm(ModelForm):
    class Meta:
        model = models.ExpensesSubCategory
        fields = ('name', 'describe', 'parent')
        labels = {
            "name": "Имя",
            "describe": "Описание",
            "parent":"Категория"
            }  


class IncomeForm(ModelForm):
    date_field = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )          
    import datetime
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 2, cur_year + 2)])
    hist_date = forms.DateField(initial=datetime.date.today() - datetime.timedelta(days=7),widget=forms.SelectDateWidget(years=year_range))
    class Meta:
        model = models.Income
        fields = ('account', 'amount', 'category','datetime')
        labels = {
            "account": "Счет",
            "amount": "Сумма",
            "category":"Категория",
            "'datetime'":"Дата"            
            }


class ExpensesForm(ModelForm):
    class Meta:
        model = models.Expenses
        fields = ('account', 'amount', 'category','datetime')
        labels = {
            "account": "Счет",
            "amount": "Сумма",
            "category":"Категория",
            "'datetime'":"Дата"
            }