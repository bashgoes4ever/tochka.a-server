# Generated by Django 3.2.5 on 2022-06-18 19:57

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20220618_2257'),
        ('base', '0002_alter_modelwithcategory_base_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryCard',
            fields=[
                ('modelwithcategory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.modelwithcategory')),
                ('title', tinymce.models.HTMLField(blank=True, verbose_name='Заголовок')),
                ('description', tinymce.models.HTMLField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, upload_to='static/img/categories/', verbose_name='Изображение')),
                ('thumb', models.ImageField(blank=True, editable=False, upload_to='static/img/categories/')),
                ('show_link', models.BooleanField(default=True, verbose_name="Показывать кнопку 'подробнее'")),
                ('custom_link', models.CharField(blank=True, max_length=64, verbose_name='Своя ссылка')),
                ('priority', models.IntegerField(default=1, verbose_name='Приоритет')),
                ('categories', models.ManyToManyField(blank=True, default=None, to='products.ProductCategory', verbose_name='Дочерние категорие, которые будут показаны')),
            ],
            options={
                'verbose_name': 'Категория на главной',
                'verbose_name_plural': 'Категории на главной',
                'ordering': ['-priority'],
            },
            bases=('base.modelwithcategory',),
        ),
    ]
