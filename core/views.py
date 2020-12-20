from django.db.models import Sum
from django.shortcuts import render, redirect
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404
from itertools import chain
from . import models, forms



def get_balance(request):
    balance = models.OnlineBalance.objects.all()
    diff = models.OnlineBalance.objects.all().aggregate(Sum('amount'))
    context = {'balance': balance, 'diff': diff['amount__sum']}
    return render(request, 'get_balance.html', context)

def base_view(request):
    return render(request, 'base.html')

def get_category(request):
    category = models.Category.objects.all()
    context = {'category': category}
    return render(request, 'get_category.html', context)


def add_category(request):
    label = 'Добавление новой категории дохода'
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_category')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.CategoryForm()
        return render(request, 'add_category.html', {'form': form, 'label':label})

def get_income_category(request):
    label = 'Статьи доходов'
    items = models.IncomeCategory.objects.all()
    return get_category_template(request, label, items) 
     
def get_expenses_category(request):
    label = 'Статьи расходов'
    items = models.ExpensesCategory.objects.all()
    return get_category_template(request, label, items)  

def get_income_sub_category(request):
    label = 'Статьи доходов'
    items = {}
    items['category'] = models.IncomeCategory.objects.all()
    items['subcategory'] = models.IncomeSubCategory.objects.all().order_by('parent')
    return get_category_template(request, label, items)     
     
def get_expenses_sub_category(request):
    label = 'Статьи расходов'
    items = {}
    items['category'] = models.ExpensesCategory.objects.all()
    items['subcategory'] = models.ExpensesSubCategory.objects.all().order_by('parent')
    return get_category_template(request, label, items)        

def get_category_template(request, label, items):
    context = {'items': items, 'label':label}
    return render(request, 'get_category.html', context)    

def add_balance(request):
    if request.method == 'POST':
        form = forms.OnlineBalanceForm(request.POST)
        if form.is_valid():
            new_balance = form.save(commit=False)
            new_balance.save()
            return redirect('get_balance')
        else:
            return render(request, 'add_balance.html', {'form': form})
    else:
        form = forms.OnlineBalanceForm()
        return render(request, 'add_balance.html', {'form': form})


def add_currency(request):
    label = 'Добавление новой валюты'
    if request.method == 'POST':
        form = forms.CurrencyForm(request.POST)
        if form.is_valid():
            new_currency = form.save(commit=False)
            new_currency.save()
            return redirect('get_currency')
        else:
            return render(request, 'add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.CurrencyForm()
        return render(request, 'add_item_form.html', {'form': form,'label':label})


def get_currency(request):
    label = 'Список доступных валют'
    items = models.Currency.objects.all()
    return render(request, 'get_currency.html', {'items':items,'label':label})


def add_account(request):
    label = 'Добавление нового счета'
    if request.method == 'POST':
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.save()
            return redirect('get_accounts')
        else:
            return render(request, 'add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.AccountForm()
        return render(request, 'add_item_form.html', {'form': form,'label':label})


def get_accounts(request):
    label = 'Список доступных счетов'
    items = models.Account.objects.all()
    return render(request, 'get_accounts.html', {'items':items,'label':label})    

def get_account(request, account_id):
    label = 'Информация о счете:'
    item = {}
    item['info'] = get_object_or_404(models.Account, pk=account_id)
    items_income = models.Income.objects.filter(account = item['info']).order_by('-datetime').annotate(type_of = Value('+', output_field=CharField()))
    items_expenses = models.Expenses.objects.filter(account = item['info']).order_by('-datetime').annotate(type_of = Value('-', output_field=CharField()))
    items = sorted(
        chain(items_income, items_expenses),
        key=lambda item: item.datetime, reverse=False)
    item['data'] = items
    items_income_amount_sum = items_income.aggregate(Sum('amount'))['amount__sum']
    items_expenses_amount_sum = items_expenses.aggregate(Sum('amount'))['amount__sum'] 
    print('amount', item['info'].amount)
    item['total'] = item['info'].amount
    item['total'] += items_income_amount_sum if items_income_amount_sum else 0
    item['total'] -= items_expenses_amount_sum if items_expenses_amount_sum else 0
    return render(request, 'get_account.html', {'item':item,'label':label}) 


def delete_account(request, account_id):
    label = 'Информация о счете:'
    item = models.Account.objects.get(id=account_id)
    item.delete()
    # message = 'Счет был успешно удален!'
    return redirect('get_accounts')    


def add_income_category(request):
    label = 'Добавление новой категории дохода'    
    if request.method == 'POST':
        form = forms.IncomeCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_income_category')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.IncomeCategoryForm()
        return render(request, 'add_category.html', {'form': form, 'label':label})

def add_expenses_category(request):
    label = 'Добавление новой категории расхода'   
    if request.method == 'POST':
        form = forms.ExpensesCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_expenses_category')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.ExpensesCategoryForm()
        return render(request, 'add_category.html', {'form': form, 'label':label})     
        
def add_income_sub_category(request):
    label = 'Добавление новой подкатегории дохода'    
    if request.method == 'POST':
        form = forms.IncomeSubCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_income_sub_category')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.IncomeSubCategoryForm()
        return render(request, 'add_category.html', {'form': form, 'label':label}) 


def add_expenses_sub_category(request):
    label = 'Добавление новой подкатегории расхода'    
    if request.method == 'POST':
        form = forms.ExpensesSubCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_expenses_sub_category')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.ExpensesSubCategoryForm()
        return render(request, 'add_category.html', {'form': form, 'label':label}) 

def add_income(request):
    label = 'Поступление средст на счет'    
    if request.method == 'POST':
        form = forms.IncomeForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_income')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.IncomeForm()
        return render(request, 'add_category.html', {'form': form, 'label':label}) 

def add_expenses(request):
    label = 'Cписание средст со счета'    
    if request.method == 'POST':
        form = forms.ExpensesForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_expenses')
        else:
            return render(request, 'add_category.html', {'form': form, 'label':label})
    else:
        form = forms.ExpensesForm()
        return render(request, 'add_category.html', {'form': form, 'label':label}) 

def get_income(request):
    items = models.Income.objects.all().order_by('datetime')
    label = 'Список поступления средст'
    return render(request, 'get_income.html', {'items':items,'label':label}) 


def get_expenses(request):
    items = models.Expenses.objects.all().order_by('datetime')
    label = 'Список списания средств'
    return render(request, 'get_income.html', {'items':items,'label':label})

def get_full(request):
    from itertools import chain
    items_income = models.Income.objects.all().order_by('datetime').annotate(type_of = Value('+', output_field=CharField()))
    items_expenses = models.Expenses.objects.all().order_by('datetime').annotate(type_of = Value('-', output_field=CharField()))
    items = sorted(
        chain(items_income, items_expenses),
        key=lambda item: item.datetime, reverse=True)
    label = 'Список всех движений средст'
    return render(request, 'get_income.html', {'items':items,'label':label}) 


def get_full___(request, account):
    from itertools import chain
    items_income = models.Income.objects.all().order_by('datetime').annotate(type_of = Value('+', output_field=CharField()))
    items_expenses = models.Expenses.objects.all().order_by('datetime').annotate(type_of = Value('-', output_field=CharField()))
    items = sorted(
        chain(items_income, items_expenses),
        key=lambda item: item.datetime, reverse=True)
    label = 'Список всех движений средст'
    return render(request, 'get_income.html', {'items':items,'label':label}) 