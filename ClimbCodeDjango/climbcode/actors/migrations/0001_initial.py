# Generated by Django 2.0.2 on 2018-03-14 18:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('name', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('surname', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('phone', models.CharField(help_text='Requerido. 9 dígitos como máximo.', max_length=9, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{3})(\\-)(\\d{3})(\\-)(\\d{3})$')])),
                ('identificationCode', models.CharField(help_text='Requerido.', max_length=9)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('userAccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Actors',
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
            ],
            options={
                'verbose_name_plural': 'Administrators',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Programmer',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
            ],
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('address', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('postalCode', models.CharField(help_text='Requerido. 5 dígitos como máximo.', max_length=95, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{5})$')])),
                ('type', models.CharField(choices=[('High School', 'High School'), ('Academy', 'Academy')], default='High School', max_length=10)),
                ('teachingType', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=20)),
            ],
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
            ],
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
            ],
            bases=('actors.actor',),
        ),
    ]
