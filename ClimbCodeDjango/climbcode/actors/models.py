from django.db import models
from django.core.validators import RegexValidator
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from subjects.models import Subject

# Create your models here.

class Actor(models.Model):
    """
    Clase que define el modelo Actor: nombre, aepllidos, teléfono, código de identificación (DNI, CIF o código del centro), foto.
    """
    name = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    surname = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    phone = models.CharField(max_length = 11, help_text = 'Requerido. 9 dígitos como máximo.',
        validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$', message = 'El formato introducido es incorrecto.')])
    identificationCode = models.CharField(max_length = 9, help_text = 'Requerido.')
    photo = models.ImageField(null = True, blank = True, upload_to = 'uploads/')

    # Relaciones
    userAccount = models.OneToOneField('auth.User', on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Actors"


class ActorAdminPanel(admin.ModelAdmin):
    """
    Clase que oculta el modelo en el panel de administración.
    """
    def get_model_perms(self, request):
        return {}


class Administrator(Actor):
    """
    Clase que define el modelo Administrador.
    """
    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Administrators"


class AdministratorAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'identificationCode')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Programmer(Actor):
    """
    Clase que define el modelo Programador.
    """
    balance = models.DecimalField(default = 0, max_digits = 9, decimal_places = 2)

    # TODO: Relación con ejercicios

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Programmers"


class ProgrammerAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Programador que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'identificationCode')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class School(Actor):
    """
    Clase que define el modelo Escuela.
    """
    # Tipos de escuela
    HIGH_SCHOOL = 'High School'
    ACADEMY = 'Academy'
    SchoolType = (
        (HIGH_SCHOOL, 'High School'),
        (ACADEMY, 'Academy')
    )

    # Tipos de enseñanza
    PUBLIC = 'Public'
    PRIVATE = 'Private'
    TeachingType = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private')
    )

    address = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    postalCode = models.CharField(max_length = 95, help_text = 'Requerido. 5 dígitos como máximo.',
        validators = [RegexValidator(regex = r'^(\d{5})$', message = 'El formato introducido es incorrecto.')])
    type = models.CharField(max_length = 10, choices = SchoolType, default = HIGH_SCHOOL)
    teachingType = models.CharField(max_length = 20, choices = TeachingType, default = PUBLIC)

    # TODO: Relaciones con los ejercicios disponibles por la asignatura
    # exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Schools"


class SchoolAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Actor-Escuela que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'identificationCode', 'type')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Teacher(Actor):
    """
    Clase que define el modelo Profesor.
    """

    # Relación con las asignaturas impartidas
    subjects = models.ManyToManyField(Subject)
    # Relación con la escuela a la que pertenece
    school_t = models.ForeignKey(School, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Teachers"


class TeacherAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Teacher que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'identificationCode')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()


class Student(Actor):
    """
    Clase que define el modelo Alumno.
    """

    # Relación con las asignaturas cursadas
    subjects = models.ManyToManyField(Subject)
    # Relación con la escuela a la que pertenece
    school_s = models.ForeignKey(School, on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.userAccount.get_full_name() + ' (' + self.userAccount.get_username() + ')'

    class Meta:
        verbose_name_plural = "Students"

class StudentAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Alumno que se mostrarán en el panel de administración.
    """
    list_display = ('userAccount', 'get_full_name', 'identificationCode')

    def get_full_name(self, obj):
        return obj.userAccount.get_full_name()

