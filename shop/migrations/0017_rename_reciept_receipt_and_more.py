# Generated by Django 4.2.1 on 2023-06-24 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_reciept_session'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reciept',
            new_name='Receipt',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='reciept',
            new_name='receipt',
        ),
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.receipt'),
            preserve_default=False,
        ),
    ]
