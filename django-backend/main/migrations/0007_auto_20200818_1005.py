# Generated by Django 3.1 on 2020-08-18 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200818_1001'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('source', 'target')},
        ),
    ]
