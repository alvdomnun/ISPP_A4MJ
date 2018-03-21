# Generated by Django 2.0.2 on 2018-03-18 13:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numUsers', models.PositiveIntegerField(default=0)),
                ('numFreeExercises', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Licenses',
            },
        ),
        migrations.CreateModel(
            name='LicenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='BASIC', help_text='Requerido. 50 carácteres como máximo.', max_length=50, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto. Debe ser BASIC, MEDIUM, LARGE', regex='^BASIC$')])),
                ('numUsers', models.PositiveIntegerField(default=0)),
                ('numFreeExercises', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name_plural': 'License Types',
            },
        ),
        migrations.AddField(
            model_name='license',
            name='licenseType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='licenses.LicenseType'),
        ),
        migrations.AddField(
            model_name='license',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='actors.School'),
        ),
    ]
