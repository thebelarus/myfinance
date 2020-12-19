from django.contrib import admin
from .models import OnlineBalance, Currency, IncomeCategory, ExpensesCategory, IncomeSubCategory, ExpensesSubCategory, Account, Income, Expenses

class OnlineBalanceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'datetime')
    list_display_links = ('amount', 'category', 'datetime')
    search_field = ('amount', 'category', 'datetime')


admin.site.register(OnlineBalance, OnlineBalanceAdmin)
admin.site.register(Currency)
admin.site.register(IncomeCategory)
admin.site.register(ExpensesCategory)
admin.site.register(IncomeSubCategory)
admin.site.register(ExpensesSubCategory)
admin.site.register(Account)
admin.site.register(Income)
admin.site.register(Expenses)