# Generated by Django 4.2.3 on 2023-08-20 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_sender_sender_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sender',
            options={'permissions': [('set_disabled', 'Can disable Рассылка')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]