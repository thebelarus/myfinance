from django.contrib import admin
from .models import Category, OnlineBalance


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'describe')
    list_display_links = ('name', 'describe')
    search_field = ('name', 'describe')


class OnlineBalanceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'datetime')
    list_display_links = ('amount', 'category', 'datetime')
    search_field = ('amount', 'category', 'datetime')


admin.site.register(Category, CategoryAdmin)
admin.site.register(OnlineBalance, OnlineBalanceAdmin)
