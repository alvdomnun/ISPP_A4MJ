# Generated by Django 2.0.2 on 2018-03-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Requerido. 50 carácteres como máximo', max_length=50, unique=True)),
                ('course', models.CharField(help_text='Requerido. 50 carácteres como máximo', max_length=50, unique=True)),
                ('code', models.CharField(help_text='Requerido. 5 carácteres como máximo', max_length=5, unique=True)),
            ],
            options={
                'verbose_name_plural': 'DefaultSubjects',
            },
        ),
    ]
