from django.contrib import admin
from .models import OnlineBalance, Currency, IncomeCategory, ExpensesCategory, IncomeSubCategory, ExpensesSubCategory, Account, Income, Expenses

admin.site.register(OnlineBalance)
admin.site.register(Currency)
admin.site.register(IncomeCategory)
admin.site.register(ExpensesCategory)
admin.site.register(IncomeSubCategory)
admin.site.register(ExpensesSubCategory)
admin.site.register(Account)
admin.site.register(Income)
admin.site.register(Expenses)