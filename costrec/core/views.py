from django.shortcuts import render
from . import models, forms


def categories(request):
    category = models.Category.objects.all()
    context = {'category': category}
    return render(request, 'some.html', context)


def online_balance(request):
    balance = models.OnlineBalance.objects.all()
    context = {'balance': balance}
    render(request, 'other.html', context)


