# Generated by Django 2.0.2 on 2018-03-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0006_auto_20180318_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='exercises',
            field=models.ManyToManyField(null=True, to='exercises.Exercise'),
        ),
    ]
