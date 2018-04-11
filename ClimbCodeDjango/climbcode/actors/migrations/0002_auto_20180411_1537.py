# Generated by Django 2.0.2 on 2018-04-11 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchaseTickets', '0001_initial'),
        ('provinces', '0001_initial'),
        ('actors', '0001_initial'),
        ('subjects', '0001_initial'),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='subjects.Subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='school_s',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='actors.School', verbose_name='School'),
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='subjects.Subject'),
        ),
        migrations.AddField(
            model_name='school',
            name='exercises',
            field=models.ManyToManyField(blank=True, through='purchaseTickets.PurchaseTicket', to='exercises.Exercise'),
        ),
        migrations.AddField(
            model_name='school',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provinces.Province'),
        ),
    ]
