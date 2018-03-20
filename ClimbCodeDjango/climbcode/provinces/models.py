from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class Province(models.Model):
    #Atributos de la clase Province: name
    name = models.CharField(max_length=50, unique=True, help_text="Requerido. 50 carácteres como máximo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"

class ProvinceAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('name',)