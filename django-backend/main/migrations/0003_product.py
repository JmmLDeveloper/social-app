# Generated by Django 3.1 on 2020-08-22 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200822_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, verbose_name='identificador del producto')),
                ('stock_number', models.IntegerField(verbose_name='Cantidad En Alamacene')),
            ],
        ),
    ]
