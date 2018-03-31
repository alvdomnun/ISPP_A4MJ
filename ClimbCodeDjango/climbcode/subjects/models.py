from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from exercises.models import Exercise

# Create your models here.

class Subject(models.Model):
    """
    Clase que define el modelo Asignatura: nombre, curso y código.
    """
    name = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    course = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')

    # Relación con la escuela a la que pertenece la asignatura
    school = models.ForeignKey('actors.School', on_delete = models.CASCADE)
    # Relación con los ejercicios categorizados por la asignatura
    exercises = models.ManyToManyField(Exercise, blank = True)

    def __str__(self):
        return self.name + ' (' + self.course + ')'

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"


class SubjectAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades de la asignatura que se mostrarán en el panel de administración.
    """
    list_display = ('name', 'course')
