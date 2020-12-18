from django.db.models import Sum
from django.shortcuts import render, redirect
from . import models, forms

def get_category(request):
    category = models.Category.objects.all()
    context = {'category': category}
    return render(request, 'categories/get_category.html', context)


def get_balance(request):
    balance = models.OnlineBalance.objects.all()
    diff = models.OnlineBalance.objects.all().aggregate(Sum('amount'))
    # print(diff)
    context = {'balance': balance, 'diff': diff['amount__sum']}
    return render(request, 'categories/get_balance.html', context)

def base_view(request):
    return render(request, 'base.html')

def add_category(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_category')
        else:
            return render(request, 'categories/add_category.html', {'form': form})
    else:
        form = forms.CategoryForm()
        return render(request, 'categories/add_category.html', {'form': form})


def add_balance(request):
    if request.method == 'POST':
        form = forms.OnlineBalanceForm(request.POST)
        if form.is_valid():
            new_balance = form.save(commit=False)
            new_balance.save()
            return redirect('get_balance')
        else:
            return render(request, 'categories/add_balance.html', {'form': form})
    else:
        form = forms.OnlineBalanceForm()
        return render(request, 'categories/add_balance.html', {'form': form})


def add_currency(request):
    label = 'Добавление новой валюты'
    if request.method == 'POST':
        form = forms.CurrencyForm(request.POST)
        if form.is_valid():
            new_currency = form.save(commit=False)
            new_currency.save()
            return redirect('get_currency')
        else:
            return render(request, 'categories/add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.CurrencyForm()
        return render(request, 'categories/add_item_form.html', {'form': form,'label':label})


def get_currency(request):
    label = 'Список доступных валют'
    items = models.Currency.objects.all()
    return render(request, 'categories/get_currency.html', {'items':items,'label':label})


def add_account(request):
    label = 'Добавление нового счета'
    if request.method == 'POST':
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.save()
            return redirect('get_account')
        else:
            return render(request, 'categories/add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.AccountForm()
        return render(request, 'categories/add_item_form.html', {'form': form,'label':label})


def get_account(request):
    label = 'Список доступных счетов'
    items = models.Account.objects.all()
    return render(request, 'categories/get_account.html', {'items':items,'label':label})    