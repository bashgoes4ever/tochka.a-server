# Generated by Django 3.2.5 on 2022-06-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210801_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hour_rate',
            field=models.BooleanField(default=False, verbose_name='Товар с почасовой оплатой'),
        ),
    ]