# Generated by Django 3.0.1 on 2022-03-08 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialKospi',
            fields=[
                ('info_kospi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='stock.InfoKospi')),
                ('face_value', models.CharField(max_length=20)),
                ('capital_stock', models.CharField(max_length=20)),
                ('number_of_listings', models.CharField(max_length=20)),
                ('credit_rate', models.CharField(max_length=20)),
                ('year_high_price', models.CharField(max_length=20)),
                ('year_low_price', models.CharField(max_length=20)),
                ('market_cap', models.CharField(max_length=20)),
                ('foreigner_percent', models.CharField(max_length=20)),
                ('substitute_price', models.CharField(max_length=20)),
                ('per', models.CharField(max_length=20)),
                ('eps', models.CharField(max_length=20)),
                ('roe', models.CharField(max_length=20)),
                ('pbr', models.CharField(max_length=20)),
                ('ev', models.CharField(max_length=20)),
                ('bps', models.CharField(max_length=20)),
                ('sales_revenue', models.CharField(max_length=20)),
                ('operating_income', models.CharField(max_length=20)),
                ('net_income', models.CharField(max_length=20)),
                ('shares_outstanding', models.CharField(max_length=20)),
                ('shares_outstanding_rate', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['info_kospi'],
            },
        ),
    ]