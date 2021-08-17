# Generated by Django 3.2.5 on 2021-08-17 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorycard',
            options={'ordering': ['-priority'], 'verbose_name': 'Категория на главной', 'verbose_name_plural': 'Категории на главной'},
        ),
        migrations.AlterField(
            model_name='categorycard',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/img/categories/', verbose_name='Изображение'),
        ),
    ]
