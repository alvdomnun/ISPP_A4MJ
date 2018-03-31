# Generated by Django 2.0.2 on 2018-03-29 18:46

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
                ('phone', models.CharField(help_text='Requerido. Patrón XXX-XXX-XXX.', max_length=11, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{3})(\\-)(\\d{3})(\\-)(\\d{3})$')])),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('userAccount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User Account')),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actores',
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Programmer',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
            ],
            options={
                'verbose_name': 'Programador',
                'verbose_name_plural': 'Programadores',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('centerName', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50, null=True)),
                ('address', models.CharField(help_text='Requerido. 50 carácteres como máximo.', max_length=50)),
                ('postalCode', models.CharField(help_text='Requerido. 5 dígitos como máximo.', max_length=5, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^(\\d{5})$')], verbose_name='Postal Code')),
                ('type', models.CharField(choices=[('High School', 'High School'), ('Academy', 'Academy')], default='High School', max_length=11)),
                ('teachingType', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Public', max_length=20, verbose_name='Teaching Type')),
                ('identificationCode', models.CharField(help_text='Requerido. CIF para escuelas; Código de Centro para academías.', max_length=9, null=True, verbose_name='CIF or Center Code')),
            ],
            options={
                'verbose_name': 'Escuela',
                'verbose_name_plural': 'Escuelas',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
            ],
            options={
                'verbose_name': 'Alumno',
                'verbose_name_plural': 'Alumnos',
            },
            bases=('actors.actor',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('actor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='actors.Actor')),
                ('dni', models.CharField(help_text='Requerido. 8 dígitos y una letra.', max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='El formato introducido es incorrecto.', regex='^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], verbose_name='D.N.I.')),
                ('school_t', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='actors.School', verbose_name='School')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
            },
            bases=('actors.actor',),
        ),
    ]
