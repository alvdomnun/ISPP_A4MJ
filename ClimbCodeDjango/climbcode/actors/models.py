from django.db import models
from django.core.validators import RegexValidator
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from subjects.models import Subject
from provinces.models import Province
from exercises.models import Exercise
import re
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


# Create your models here.

class Actor(models.Model):
    """
    Clase que define el modelo Actor: nombre, aepllidos, teléfono, foto.
    """
    phone = models.CharField(max_length = 9, help_text = 'Requerido. Patrón de 9 dígitos.',
        validators = [RegexValidator(regex = r'^(\d{9})$', message = 'El formato introducido es incorrecto.')])
    photo = models.ImageField(null = True, blank = True, upload_to = 'uploads/')

    # Relaciones
    userAccount = models.OneToOneField('auth.User', verbose_name = 'User Account', on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actores"


class ActorAdminPanel(admin.ModelAdmin):
    """
    Clase que oculta el modelo Actor en el panel de administración.
    """
    def get_model_perms(self, request):
        return {}


class Administrator(Actor):
    """
    Clase que define el modelo Administrador.
    """
    dni = models.CharField(verbose_name = 'D.N.I.', max_length = 9, null = True, help_text = 'Requerido. 8 dígitos y una letra.',
        validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$', message = 'El formato introducido es incorrecto.')])

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"


class AdministratorAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Programmer(Actor):
    """
    Clase que define el modelo Programador.
    """
    balance = models.DecimalField(default = 0, max_digits = 9, decimal_places = 2)
    dni = models.CharField(verbose_name = 'D.N.I.', max_length = 9, null = True, help_text = 'Requerido. 8 dígitos y una letra.',
        validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$', message = 'El formato introducido es incorrecto.')])

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    def full_clean(self, exclude=None, validate_unique=True):
        if not validate(self.dni):
            raise ValidationError({
                NON_FIELD_ERRORS: ['El DNI tiene un formato incorrecto', ],
            })

    class Meta:
        verbose_name = "Programador"
        verbose_name_plural = "Programadores"


class ProgrammerAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Programador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni', 'balance')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class School(Actor):
    """
    Clase que define el modelo Escuela.
    """
    # Tipos de escuela
    HIGH_SCHOOL = 'Instituto'
    ACADEMY = 'Academia'
    SchoolType = (
        (HIGH_SCHOOL, 'Instituto'),
        (ACADEMY, 'Academia')
    )

    # Tipos de enseñanza
    PUBLIC = 'Público'
    PRIVATE = 'Privado'
    TeachingType = (
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado')
    )

    centerName = models.CharField(max_length = 50, null = True, help_text = 'Requerido. 50 carácteres como máximo.')
    address = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    postalCode = models.CharField(verbose_name = 'Postal Code', max_length = 5, help_text = 'Requerido. 5 dígitos como máximo.',
        validators = [RegexValidator(regex = r'^(\d{5})$', message = 'El formato introducido es incorrecto.')])
    type = models.CharField(max_length = 11, choices = SchoolType, default = HIGH_SCHOOL)
    teachingType = models.CharField(verbose_name = 'Teaching Type', max_length = 20, choices = TeachingType, default = PUBLIC)
    identificationCode = models.CharField(verbose_name = 'CIF or Center Code', max_length = 9,validators = [RegexValidator(regex = r'^(\d{8,9})$',
           message = 'El código de identificación debe estar compuesto de 8 dígitos o 9 dígitos.')],
           null = True, help_text = 'Requerido. CIF para escuelas; Código de Centro para academías.')
    isPayed = models.BooleanField(verbose_name = 'Pagada', default = False)

    # Relación con los ejercicios comprados
    exercises = models.ManyToManyField(Exercise, through = 'purchaseTickets.PurchaseTicket', blank = True)
    # Relación con la provincia
    province = models.ForeignKey(Province, on_delete = models.SET_NULL, null = True)
            
    def __str__(self):
        return self.centerName + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name = "Escuela"
        verbose_name_plural = "Escuelas"


class SchoolAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Actor-Escuela que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'centerName', 'identificationCode', 'type')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Teacher(Actor):
    """
    Clase que define el modelo Profesor.
    """
    dni = models.CharField(verbose_name = 'D.N.I.', max_length = 9, null = True, help_text = 'Requerido. 8 dígitos y una letra.',
        validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$', message = 'El formato introducido es incorrecto.')])

    # Relación con la escuela a la que pertenece
    school_t = models.ForeignKey(School, verbose_name = 'School', on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    def full_clean(self, exclude=None, validate_unique=True):
        if not validate(self.dni):
            raise ValidationError({
                NON_FIELD_ERRORS: ['El DNI tiene un formato incorrecto', ],
            })

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"


class TeacherAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Teacher que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni', 'school_t')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()

from django import forms

class Student(Actor):
    """
    Clase que define el modelo Alumno.
    """
    dni = models.CharField(verbose_name = 'D.N.I.', max_length = 9, null = True, help_text = 'Requerido. 8 dígitos y una letra.',
        validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$', message = 'El formato introducido es incorrecto.')])

    # Relación con la escuela a la que pertenece
    school_s = models.ForeignKey(School, verbose_name = 'School', on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    def full_clean(self, exclude=None, validate_unique=True):
        if not validate(self.dni):
            raise ValidationError({
                NON_FIELD_ERRORS: ['El DNI tiene un formato incorrecto', ],
            })

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

class StudentAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Alumno que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'dni', 'school_s')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


from stdnum.exceptions import *
from stdnum.util import clean

def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    return 'TRWAGMYFPDXBNJZSQVHLCKE'[int(number) % 23]


def validate(number):
    """Check if the number provided is a valid DNI number. This checks the
    length, formatting and check digit."""
    number = compact(number)
    if not number[:-1].isdigit():
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid DNI number. This checks the
    length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
