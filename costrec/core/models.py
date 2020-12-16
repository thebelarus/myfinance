from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 150, verbose_name='name')
    describe = models.TextField()

class OnlineBalance(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places=2, verbose_name='amount')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='datetime')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
