# Generated by Django 4.1.3 on 2023-01-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nse_app', '0002_remove_nse_setting_quantity_bn'),
    ]

    operations = [
        migrations.AddField(
            model_name='nse_setting',
            name='quantity_bn',
            field=models.FloatField(default=1, null=True),
        ),
    ]
