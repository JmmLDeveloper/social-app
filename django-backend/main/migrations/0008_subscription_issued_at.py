# Generated by Django 3.1 on 2020-08-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200818_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='issued_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
