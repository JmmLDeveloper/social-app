# Generated by Django 3.1 on 2020-08-18 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_subscription_issued_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='issued_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)),
            preserve_default=False,
        ),
    ]
