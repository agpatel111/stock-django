# Generated by Django 4.1.3 on 2023-01-05 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dropdown_stock_name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pcr', models.FloatField(null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('PE_CE_diffrent', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='live',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='nse_setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=50)),
                ('profit_percentage', models.IntegerField()),
                ('loss_percentage', models.IntegerField()),
                ('set_pcr', models.FloatField()),
                ('baseprice_plus', models.IntegerField()),
                ('quantity_bn', models.FloatField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='pcr_stock_name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pcr', models.FloatField(null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('PE_CE_diffrent', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='stock_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_strike_price', models.FloatField()),
                ('live_Strike_price', models.FloatField()),
                ('buy_price', models.FloatField()),
                ('sell_price', models.FloatField()),
                ('stop_loseprice', models.FloatField()),
                ('live_brid_price', models.FloatField()),
                ('exit_price', models.FloatField(null=True)),
                ('buy_time', models.DateTimeField(auto_now_add=True)),
                ('sell_buy_time', models.DateTimeField(null=True)),
                ('status', models.CharField(blank=True, choices=[('BUY', 'BUY'), ('SELL', 'SELL'), ('empty', 'empty')], default='empty', max_length=50)),
                ('final_status', models.CharField(blank=True, choices=[('PROFIT', 'PROFIT'), ('LOSS', 'LOSS'), ('NA', 'NA')], default='NA', max_length=50)),
                ('admin_call', models.BooleanField(default=False)),
                ('call_put', models.CharField(blank=True, choices=[('CALL', 'CALL'), ('PUT', 'PUT'), ('NA', 'NA')], max_length=50)),
                ('stock_name', models.TextField(blank=True, null=True)),
                ('squareoff', models.FloatField(blank=True, null=True)),
                ('stoploss', models.FloatField(blank=True, null=True)),
                ('percentage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nse_app.nse_setting')),
            ],
        ),
    ]
