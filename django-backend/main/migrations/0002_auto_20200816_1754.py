# Generated by Django 3.1 on 2020-08-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(default='just for testing', max_length=128),
        ),
    ]