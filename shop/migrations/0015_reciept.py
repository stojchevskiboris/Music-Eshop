# Generated by Django 4.2.1 on 2023-06-23 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_order_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reciept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciept', models.IntegerField()),
            ],
        ),
    ]
