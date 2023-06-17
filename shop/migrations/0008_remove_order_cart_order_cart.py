# Generated by Django 4.2.1 on 2023-06-16 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_cart_discount_cart_totalprice_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(to='shop.cart'),
        ),
    ]