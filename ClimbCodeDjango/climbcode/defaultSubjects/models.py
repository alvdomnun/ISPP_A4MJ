from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class DefaultSubject(models.Model):
    #Atributos de la clase DefaultSubject: name, course
    name = models.CharField(max_length = 50, help_text="Requerido. 50 carácteres como máximo")
    course = models.CharField(max_length = 50, help_text="Requerido. 50 carácteres como máximo")

    def __str__(self):
        return self.name +' ' + self.course + 'º'

    class Meta:
        verbose_name = "Asignatura Genérica"
        verbose_name_plural = "Asignaturas Genéricas"
        

class DefaultSubjectAdminPanel(admin.ModelAdmin):
    #Panel de admin
    list_display = ('name' , 'course')
