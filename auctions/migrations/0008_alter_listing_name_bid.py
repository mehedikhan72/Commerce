# Generated by Django 4.1.1 on 2022-10-05 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment_commented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.FloatField()),
                ('bid_item', models.ForeignKey(db_column='name', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bid_item', to='auctions.listing', to_field='name')),
                ('current_bidder', models.ForeignKey(db_column='username', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='current_bidder', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]
