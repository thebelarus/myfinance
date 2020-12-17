from django.shortcuts import render, redirect
from . import models, forms


def categories(request):
    category = models.Category.objects.all()
    context = {'category': category}
    return render(request, 'some.html', context)


def online_balance(request):
    balance = models.OnlineBalance.objects.all()
    context = {'balance': balance}
    render(request, 'expenses.html', context)


def add_category(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('some.html')
        else:
            return render(request, 'categories/new_category.html', {'form': form})
    else:
        form = forms.CategoryForm()
        return render(request, 'categories/new_category.html', {'form': form})


def add_balance(request):
    if request.method == 'POST':
        form = forms.OnlineBalanceForm(request.POST)
        if form.is_valid():
            new_balance = form.save(commit=False)
            new_balance.save()
            return redirect('expenses.html')
        else:
            return render(request, 'add_exp.html', {'form': form})
    else:
        form = forms.OnlineBalanceForm()
        return render(request, 'add_exp.html', {'form': form})
