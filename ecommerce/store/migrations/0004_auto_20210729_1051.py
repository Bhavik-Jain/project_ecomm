# Generated by Django 3.2.5 on 2021-07-29 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_shippingaddress_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='phone',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
