from django.db.models import Sum
from django.shortcuts import render, redirect
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from datetime import datetime
from itertools import chain
from . import models, forms
import io

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
            return render(request, 'add_item_form.html', {'form': form, 'label':label})
    else:
        form = forms.CategoryForm()
        return render(request, 'add_item_form.html', {'form': form, 'label':label})

def get_income_category(request):
    label = 'Статьи доходов'
    items = models.IncomeCategory.objects.all()
    return get_category_template(request, label, items, prefix='income') 
     
def get_expenses_category(request):
    label = 'Статьи расходов'
    items = models.ExpensesCategory.objects.all()
    return get_category_template(request, label, items, prefix='expenses')  

def delete_income_category(request, category_id):
    item = get_object_or_404(models.IncomeCategory, pk=category_id)
    item.delete()
    return redirect('get_income_category')
     
def delete_expenses_category(request, category_id):
    item = get_object_or_404(models.ExpensesCategory, pk=category_id)
    item.delete()    
    return redirect('get_expenses_category')

def delete_income_sub_category(request, category_id):
    item = get_object_or_404(models.IncomeSubCategory, pk=category_id)
    item.delete()
    return redirect('get_income_sub_category')
     
def delete_expenses_sub_category(request, category_id):
    item = get_object_or_404(models.ExpensesSubCategory, pk=category_id)
    item.delete()    
    return redirect('get_expenses_sub_category')

def get_income_sub_category(request):
    label = 'Статьи доходов'
    items = {}
    items['category'] = models.IncomeCategory.objects.all()
    items['subcategory'] = models.IncomeSubCategory.objects.all().order_by('parent')
    return get_category_template(request, label, items, prefix='income')     
     
def get_expenses_sub_category(request):
    label = 'Статьи расходов'
    items = {}
    items['category'] = models.ExpensesCategory.objects.all()
    items['subcategory'] = models.ExpensesSubCategory.objects.all().order_by('parent')
    return get_category_template(request, label, items, prefix='expenses')        


def get_category_template(request, label, items, prefix):
    context = {'items': items, 'label':label, 'prefix':prefix}
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
        # else:
        #     return render(request, 'add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.CurrencyForm()
        items = models.Currency.objects.all()
        return render(request, 'add_item_form.html', {'form': form,'label':label, 'items':items})


def get_currency(request):
    label = 'Список доступных валют'
    items = models.Currency.objects.all()
    return render(request, 'get_currency.html', {'items':items,'label':label})

def delete_currency(request, currency_id):
    item = get_object_or_404(models.Currency, pk=currency_id)
    item.delete()
    return redirect('get_currency')

def add_account(request):
    label = 'Добавление нового счета'
    if request.method == 'POST':
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.save()
        return redirect('get_accounts')
        # else:
        #     return render(request, 'add_item_form.html', {'form': form,'label':label})
    else:
        form = forms.AccountForm()
        items = models.Account.objects.all()
        return render(request, 'add_item_form.html', {'form': form,'label':label, 'items':items})


def get_accounts(request):
    label = 'Список доступных счетов'
    items = models.Account.objects.all()
    return render(request, 'get_accounts.html', {'items':items,'label':label})    

def get_account(request, account_id):
    label = 'Информация о счете:'
    item = get_account_data(account_id)
    return render(request, 'get_account.html', {'item':item,'label':label}) 

def get_account_data(account_id):
    item = {}
    item['info'] = get_object_or_404(models.Account, pk=account_id)
    item['info'] = models.Account.objects.get(pk=account_id)
    items_income = models.Income.objects.filter(account = item['info']).order_by('-datetime').annotate(type_of = Value('+', output_field=CharField()),prefix = Value('income', output_field=CharField()))
    items_expenses = models.Expenses.objects.filter(account = item['info']).order_by('-datetime').annotate(type_of = Value('-', output_field=CharField()),prefix = Value('expenses', output_field=CharField()))
    items = sorted(
        chain(items_income, items_expenses),
        key=lambda item: item.datetime, reverse=False)
    item['data'] = items
    items_income_amount_sum = items_income.aggregate(Sum('amount'))['amount__sum']
    items_expenses_amount_sum = items_expenses.aggregate(Sum('amount'))['amount__sum'] 
    item['total'] = item['info'].amount
    item['total'] += items_income_amount_sum if items_income_amount_sum else 0
    item['total'] -= items_expenses_amount_sum if items_expenses_amount_sum else 0    
    return item

def delete_account(request, account_id):
    label = 'Информация о счете:'
    item = models.Account.objects.get(id=account_id)
    item.delete()
    return redirect('get_accounts')    


def account_to_pdf_export(request, account_id):
    label = 'Информация о счете:'
    item = get_account_data(account_id)
    import datetime
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    datetime_now = datetime.datetime.now()
    datetime_str = datetime.datetime.strftime(datetime_now,'%d.%m.%Y %H:%M:%S')

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p.setFont('Arial', 16)
    p.drawString(100, 770, 'Выписка по счету: "{}" на {}'.format(
        str(item['info'].name),
        datetime_str
        ))
    p.setFont('Arial', 12)
    p.drawString(100, 700, 'Валюта: {}'.format(str(item['info'].currency)))
    p.drawString(100, 680, 'Дата создания счета: {}'.format(datetime.datetime.strftime(item['info'].datetime,'%H:%M:%S %d.%m.%Y')))
    p.drawString(100, 660, 'Начальный баланс: {}'.format(str(item['info'].amount)))
    p.drawString(100, 640, 'Текущий баланс: {}'.format(str(item['total'])))
    p.drawString(100, 620, 'Таблица операций со счетом:')
    p.setFont('Arial', 8)
    data = []
    data.append(('Категория:',
        'Тип операции',
        'Дата добавления:',
        'Сумма:'))
    data.append(('создание счета',
        'начальный баланс',
        '{}'.format(datetime.datetime.strftime(item['info'].datetime,'%d.%m.%Y %H:%M:%S')),
        str(item['info'].amount)))

    for data_item in item['data']:
        data.append((data_item.category,
            'зачисление' if data_item.prefix == 'income' else 'cписание',
            datetime.datetime.strftime(data_item.datetime,'%d.%m.%Y %H:%M:%S'),
            data_item.amount,            
            ))
    data.append(('',
        '',
        'Итого:',
        str(item['total'])))
    data_length = len(data)
    width = 300
    height = 100
    x = 100
    y = 500 - data_length*5
    f = Table(data)
    
    f.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('BOX',(0,0),(-1,-1),.5,colors.black),
        ('GRID',(0,0),(-1,0),.5,colors.black),
        ('LINEBEFORE',(0,0),(-1,-1),.5,colors.black),
        ('LINEAFTER',(-1,0),(-1,-1),.5,colors.black),
        ('LINEBELOW',(0,'splitlast'),(-1,'splitlast'),.5,colors.black)
        ]))

    f.wrapOn(p, width, height)
    f.drawOn(p, x, y)
        # <td>
        # {% if data_item.type_of %}
        #     {% if data_item.type_of == '+' %}
        #         <span style="color: green">
        #     {% else %}
        #         <span style="color: red">
        #     {% endif %}
        #     {{ data_item.type_of}}{{ data_item.amount}}</span>
        # {% else %}
        #     {{ data_item.type_of}}{{ data_item.amount}}
        # {% endif %}

    p.showPage()
    p.save()
    buffer.seek(0)
    feliename = 'Отчет_на_{}.pdf'.format(datetime.datetime.strftime(datetime_now,'%d%m%Y_%H%M%S'))
    return FileResponse(buffer, as_attachment=True, filename=feliename)


def add_income_category(request):
    label = 'Добавление новой категории дохода'    
    if request.method == 'POST':
        form = forms.IncomeCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
        return redirect('add_income_category')
    else:
        form = forms.IncomeCategoryForm()
        items = models.IncomeCategory.objects.all()
        return render(request, 'add_item_form.html', {'form': form, 'items':items, 'label':label})

def add_expenses_category(request):
    label = 'Добавление новой категории расхода'   
    if request.method == 'POST':
        form = forms.ExpensesCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
        return redirect('add_expenses_category')
    else:
        form = forms.ExpensesCategoryForm()
        items = models.ExpensesCategory.objects.all()
        return render(request, 'add_item_form.html', {'form': form, 'items':items, 'label':label})     
        
def add_income_sub_category(request):
    label = 'Добавление новой подкатегории дохода'    
    if request.method == 'POST':
        form = forms.IncomeSubCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_income_sub_category')
        else:
            return render(request, 'add_item_form.html', {'form': form, 'label':label})
    else:
        form = forms.IncomeSubCategoryForm()
        return render(request, 'add_item_form.html', {'form': form, 'label':label}) 


def add_expenses_sub_category(request):
    label = 'Добавление новой подкатегории расхода'    
    if request.method == 'POST':
        form = forms.ExpensesSubCategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_expenses_sub_category')
        else:
            return render(request, 'add_item_form.html', {'form': form, 'label':label})
    else:
        form = forms.ExpensesSubCategoryForm()
        return render(request, 'add_item_form.html', {'form': form, 'label':label}) 


def add_income(request):
    label = 'Поступление средст на счет'    
    if request.method == 'POST':
        form = forms.IncomeForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_income')
        else:
            return render(request, 'add_item_form.html', {'form': form, 'label':label})
    else:
        form = forms.IncomeForm()
        return render(request, 'add_item_form.html', {'form': form, 'label':label}) 


def delete_income(request, income_id):
    item = get_object_or_404(models.Income, pk=income_id)
    item.delete()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_expenses(request, expenses_id):
    item = get_object_or_404(models.Expenses, pk=expenses_id)
    item.delete()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   

def add_expenses(request):
    label = 'Cписание средст со счета'    
    if request.method == 'POST':
        form = forms.ExpensesForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.save()
            return redirect('get_expenses')
        else:
            return render(request, 'add_item_form.html', {'form': form, 'label':label})
    else:
        form = forms.ExpensesForm()
        return render(request, 'add_item_form.html', {'form': form, 'label':label}) 

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