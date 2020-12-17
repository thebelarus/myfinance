from django.db.models import Sum
from django.shortcuts import render, redirect
from . import models, forms


def get_category(request):
    category = models.Category.objects.all()
    context = {'category': category}
    return render(request, 'categories/get_category.html', context)


def get_balance(request):
    balance = models.OnlineBalance.objects.all()
    diff = models.OnlineBalance.objects.all().agreggate(Sum('amount'))
    context = {'balance': balance, 'diff': diff}
    render(request, 'categories/get_balance.html', context)


def add_category(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('categories/get_category.html')
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
            return redirect('categories/get_balance.html')
        else:
            return render(request, 'categories/add_balance.html', {'form': form})
    else:
        form = forms.OnlineBalanceForm()
        return render(request, 'categories/add_balance.html', {'form': form})
