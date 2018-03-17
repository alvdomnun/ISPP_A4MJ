from django.core.validators import RegexValidator
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class LicenseType(models.Model):
    #Atributos de la clase LicenseType: name, numUsers, numFreeExercises, price

    #Tipos de licencia(name): Basic, Medium, Large
    name =models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.',default= 'BASIC',
        validators = [RegexValidator(regex = r'^BASIC$' or '^MEDIUM$' or r'^LARGE$' , message = 'El formato introducido es incorrecto. Debe ser BASIC, MEDIUM, LARGE')])
    numUsers = models.PositiveIntegerField(default=0)
    numFreeExercises = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 2)

    #Sin relaciones

    def __str__(self):
        return self.name + ' - ' + self.numUsers + ' - ' + self.numFreeExercises + ' -- ' + self.price

    class Meta:
        verbose_name_plural = "LicenseTypes"


class LicenseTypeAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('name', 'numUsers','numFreeExercises', 'price')
