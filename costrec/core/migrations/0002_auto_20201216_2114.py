# Generated by Django 3.1.4 on 2020-12-16 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount'),
        ),
    ]
