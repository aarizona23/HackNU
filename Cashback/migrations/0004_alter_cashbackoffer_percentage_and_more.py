# Generated by Django 5.0.4 on 2024-04-13 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cashback', '0003_criteria_bank_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbackoffer',
            name='percentage',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='cashbackoffer',
            name='valid_from',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='cashbackoffer',
            name='valid_to',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='min_purchase_amount',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]