# Generated by Django 4.2.1 on 2023-06-26 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_receipt_discountpercent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
