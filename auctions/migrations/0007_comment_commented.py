# Generated by Django 4.1.1 on 2022-10-04 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_comment_comm_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]