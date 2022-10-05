# Generated by Django 4.1.1 on 2022-10-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_user_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comm', models.ManyToManyField(blank=True, related_name='comm', to='auctions.listing')),
            ],
        ),
    ]
