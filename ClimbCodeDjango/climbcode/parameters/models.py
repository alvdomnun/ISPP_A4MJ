from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.


class Parameter(models.Model):
    # Atributos de la clase Parameter: id
    id = models.PositiveIntegerField(default=0,primary_key=True)

    #Relación ManyToOne con Code
    code = models.ForeignKey('boxes.Code', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "Parameters"


class ParameterAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('id',)

