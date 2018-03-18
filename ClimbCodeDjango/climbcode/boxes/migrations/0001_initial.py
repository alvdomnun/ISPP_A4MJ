# Generated by Django 2.0.2 on 2018-03-18 13:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'Boxes',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.PositiveIntegerField(default=0, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('box_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxes.Box')),
            ],
            options={
                'verbose_name_plural': 'Codes',
            },
            bases=('boxes.box',),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('box_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxes.Box')),
            ],
            options={
                'verbose_name_plural': 'Pictures',
            },
            bases=('boxes.box',),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('box_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='boxes.Box')),
            ],
            options={
                'verbose_name_plural': 'Texts',
            },
            bases=('boxes.box',),
        ),
        migrations.AddField(
            model_name='box',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exercises.Exercise'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='boxes.Code'),
        ),
    ]
