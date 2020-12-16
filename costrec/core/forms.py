from django.forms import ModelForm
from . import models

class BalanceForm(ModelForm):
    class Meta:
        model = models.Balance
        field = ('amount', 'datetime', 'reason')