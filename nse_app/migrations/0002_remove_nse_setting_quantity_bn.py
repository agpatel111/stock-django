# Generated by Django 4.1.3 on 2023-01-05 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nse_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nse_setting',
            name='quantity_bn',
        ),
    ]
