# Generated by Django 4.2.1 on 2023-06-21 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_instrument_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='type',
            field=models.CharField(choices=[('Violina', 'Виолина'), ('Gitara', 'Гитара'), ('Kontrabas', 'Контрабас'), ('Harfa', 'Харфа'), ('Mandolina', 'Мандолина'), ('Violoncelo', 'Виолончело'), ('Flejta', 'Флејта'), ('Klarinet', 'Кларинет'), ('Truba', 'Труба'), ('Saksofon', 'Саксофон'), ('Tapani', 'Тапани'), ('Ksilofon', 'Ксилофон'), ('Kahoni', 'Кахони'), ('Pijano', 'Пијано'), ('Harmonika', 'Хармоника'), ('Sintisajzer', 'Синтисајзер')], default='Gitara', max_length=12),
        ),
    ]
