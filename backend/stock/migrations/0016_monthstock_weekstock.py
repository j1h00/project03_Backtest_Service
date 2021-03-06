# Generated by Django 3.0.1 on 2022-03-21 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0015_interest'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthStock',
            fields=[
                ('stock_seq', models.AutoField(primary_key=True, serialize=False)),
                ('code_number', models.CharField(max_length=10)),
                ('current_price', models.CharField(blank=True, max_length=20, null=True)),
                ('changes', models.CharField(blank=True, max_length=20, null=True)),
                ('chages_ratio', models.CharField(blank=True, max_length=20, null=True)),
                ('start_price', models.CharField(blank=True, max_length=20, null=True)),
                ('high_price', models.CharField(blank=True, max_length=20, null=True)),
                ('low_price', models.CharField(blank=True, max_length=20, null=True)),
                ('volume', models.CharField(blank=True, max_length=20, null=True)),
                ('trade_price', models.CharField(blank=True, max_length=50, null=True)),
                ('market_cap', models.CharField(blank=True, max_length=50, null=True)),
                ('stock_amount', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'month_stock',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WeekStock',
            fields=[
                ('stock_seq', models.AutoField(primary_key=True, serialize=False)),
                ('code_number', models.CharField(max_length=10)),
                ('current_price', models.CharField(blank=True, max_length=20, null=True)),
                ('changes', models.CharField(blank=True, max_length=20, null=True)),
                ('chages_ratio', models.CharField(blank=True, max_length=20, null=True)),
                ('start_price', models.CharField(blank=True, max_length=20, null=True)),
                ('high_price', models.CharField(blank=True, max_length=20, null=True)),
                ('low_price', models.CharField(blank=True, max_length=20, null=True)),
                ('volume', models.CharField(blank=True, max_length=20, null=True)),
                ('trade_price', models.CharField(blank=True, max_length=50, null=True)),
                ('market_cap', models.CharField(blank=True, max_length=50, null=True)),
                ('stock_amount', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'week_stock',
                'managed': False,
            },
        ),
    ]
