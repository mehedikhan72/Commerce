# Generated by Django 4.1.1 on 2022-10-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_name_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='first_bid_made',
            field=models.BooleanField(default=False),
        ),
    ]
