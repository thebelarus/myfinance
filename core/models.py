from django.db import models

class Category(models.Model):
    name = models.CharField(unique = True, max_length = 150, verbose_name='name')
    
    def __str__(self):
        return self.name

class Currency(models.Model):
    ''' Модель для описания валюты
    Поля:
        name - имя валюты, например(Доллар США, Белорусский рубль)
        currency_code - международный код валюты, например(BYN, USD, EUR, PLN, RUB, AUD)
        code - графический символ валюты, например($, €, ₽). Может отсутствовать.
    '''
    name = models.CharField(unique = True, max_length = 15, verbose_name='name',)
    currency_code = models.CharField(max_length = 4, verbose_name='currency_code') 
    code = models.CharField(max_length = 1, verbose_name='code')

    def __str__(self):
        return '{}({})'.format(self.name, self.code)
 
    class Meta:
        verbose_name = 'Валюта'   
        verbose_name_plural = 'Валюты'  

class IncomeCategory(Category):
    pass

class ExpensesCategory(Category):
    pass 

class IncomeSubCategory(Category):
    parent = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    describe = models.TextField()

    class Meta:
        ordering = ["parent"]

class ExpensesSubCategory(Category):
    parent = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    describe = models.TextField()

    class Meta:
        ordering = ["parent"]

class Account(models.Model):
    '''Модель для описания конкретного кошелька
    Поля:
        имя
        валюта
        дата 
        сумма
        описание
    '''
    name = models.CharField(unique = True, max_length = 30, verbose_name='name',)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='currency',)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')
    amount = models.DecimalField(max_digits = 15, decimal_places=2, verbose_name='amount')
    
    def __str__(self):
        return str(self.name) 

    class Meta:
        verbose_name = 'Счет'   
        verbose_name_plural = 'Счета'    


class IncomeExpensesBase(models.Model):
    datetime = models.DateTimeField(verbose_name='datetime')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)   
    amount = models.DecimalField(max_digits = 15, decimal_places=2, verbose_name='amount')


class Income(IncomeExpensesBase):
    ''' Модель для описания всех поступления средст '''
    category = models.ForeignKey(IncomeSubCategory, on_delete=models.CASCADE)


class Expenses(IncomeExpensesBase):
    ''' Модель для описания всех списаний средст '''    
    category = models.ForeignKey(ExpensesSubCategory, on_delete=models.CASCADE)

class OnlineBalance(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places=2, verbose_name='amount')
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True,)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')