# Generated by Django 4.2.7 on 2023-11-14 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_image_alter_product_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_ordered']},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-date_added']},
        ),
    ]