# Generated by Django 4.2.3 on 2023-08-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='Электронная почта'),
        ),
    ]
