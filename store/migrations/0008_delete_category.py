# Generated by Django 4.2.7 on 2023-11-17 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_orderitem_cartitem_order_shipping'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
