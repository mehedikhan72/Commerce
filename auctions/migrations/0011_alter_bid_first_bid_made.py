# Generated by Django 4.1.2 on 2022-10-05 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_bid_first_bid_made'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='first_bid_made',
            field=models.BooleanField(default=False),
        ),
    ]
