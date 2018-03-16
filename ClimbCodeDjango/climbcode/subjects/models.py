from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class Subject(models.Model):
    """
    Clase que define el modelo Asignatura: nombre, curso y código.
    """
    name = models.CharField(max_length = 50, unique = True, help_text = 'Requerido. 50 carácteres como máximo.')
    course = models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.')
    code = models.CharField(max_length = 50, help_text = 'Requerido.')

    # Relación con la escuela a la que pertenece la asignatura
    school = models.ForeignKey('actors.School', on_delete = models.CASCADE)
    # TODO: Aclarar conceptualmente. Relación con los ejercicios categorizados por la asignatura
    # exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name + ' - ' + self.course + ' (' + self.code + ')'

    class Meta:
        verbose_name_plural = "Subjects"


class SubjectAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades de la asignatura que se mostrarán en el panel de administración.
    """
    list_display = ('name', 'course', 'code')
