# Generated by Django 2.0.2 on 2018-03-18 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0010_auto_20180318_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='actor',
            name='surname',
        ),
    ]
