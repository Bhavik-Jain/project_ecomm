# Generated by Django 3.2.5 on 2021-08-07 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='customer',
        ),
    ]