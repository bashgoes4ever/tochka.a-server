# Generated by Django 3.2.5 on 2021-09-12 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=64, verbose_name='Относительная ссылка на страницу')),
                ('title', models.CharField(max_length=64, verbose_name='Title')),
                ('keywords', models.TextField(blank=True, max_length=64, null=True, verbose_name='Keywords')),
                ('description', models.TextField(blank=True, max_length=64, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Мета данные',
                'verbose_name_plural': 'Мета данные',
            },
        ),
    ]
