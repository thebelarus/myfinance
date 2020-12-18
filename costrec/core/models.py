from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 150, verbose_name='name')
    describe = models.TextField()
    
    def __str__(self):
        return self.name

class OnlineBalance(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places=2, verbose_name='amount')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')

class Currency(models.Model):
    ''' Модель для описания валюты
    Поля:
        name - имя валюты, например(Доллар США, Белорусский рубль)
        currency_code - международный код валюты, например(BYN, USD, EUR, PLN, RUB, AUD)
        code - графический символ валюты, например($, €, ₽). Может отсутствовать.
    '''
    name = models.CharField(max_length = 15, verbose_name='name',)
    currency_code = models.CharField(max_length = 4, verbose_name='currency_code') 
    code = models.CharField(max_length = 1, verbose_name='code')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Валюта'   
        verbose_name_plural = 'Валюты'  

class IncomeCategory(Category):
    pass

class ExpensesCategory(Category):
    pass 

class IncomeSubCategory(Category):
    parent = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

class ExpensesSubCategory(Category):
    parent = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)

class Account(models.Model):
    '''Модель для описания конкретного кошелька
    Поля:
        имя
        валюта
        дата 
        сумма
        описание
    '''
    name = models.CharField(max_length = 30, verbose_name='name',)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='currency',)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')
    amount = models.DecimalField(max_digits = 15, decimal_places=2, verbose_name='amount')
    
    def __str__(self):
        return str(self.currency) + str(self.amount) + str(self.datetime) 

    class Meta:
        verbose_name = 'Счет'   
        verbose_name_plural = 'Счета'    


class IncomeExpensesBase(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)   
    amount = models.DecimalField(max_digits = 15, decimal_places=2, verbose_name='amount')

class Income(IncomeExpensesBase):
    ''' Модель для описания всех поступления средст '''
    category = models.ForeignKey(IncomeSubCategory, on_delete=models.CASCADE)



class Expenses(IncomeExpensesBase):
    ''' Модель для описания всех списаний средст '''    
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
