# Generated by Django 4.1.2 on 2022-10-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_bid_current_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='current_bidder',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
