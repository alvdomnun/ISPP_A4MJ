# Generated by Django 2.0.2 on 2018-03-18 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='exercises',
            field=models.ManyToManyField(blank=True, to='exercises.Exercise'),
        ),
    ]
