# Generated by Django 5.0.4 on 2024-04-13 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cashback', '0004_alter_cashbackoffer_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashbackoffer',
            name='percentage',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
