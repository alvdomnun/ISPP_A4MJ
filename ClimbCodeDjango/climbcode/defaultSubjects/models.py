from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class DefaultSubject(models.Model):
    #Atributos de la clase DefaultSubject: name, course
    name = models.CharField(max_length = 50, unique=True, help_text="Requerido. 50 carácteres como máximo")
    course = models.CharField(max_length = 50, unique=True, help_text="Requerido. 50 carácteres como máximo")
    code = models.CharField(max_length = 5, unique=True, help_text="Requerido. 5 carácteres como máximo")

    def __str__(self):
        return self.name + ' - ' + self.course

    class Meta:
        verbose_name_plural = "Default Subjects"
        

class DefaultSubjectAdminPanel(admin.ModelAdmin):
    #Panel de admin
    list_display = ('name' , 'course')
