from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.

class ElementPrice(models.Model):
    #Atributos de la clase ElementPrice: buyExerciseValue, promoteExerciseValue
    buyExerciseValue = models.DecimalField(default = 4.0, max_digits = 9, decimal_places = 2)
    promoteExerciseValue = models.DecimalField(default = 1.0, max_digits = 9, decimal_places = 2)
    #Sin relaciones

    def __str__(self):
        return self.buyExerciseValue + ' - ' + self.promoteExerciseValue

    class Meta:
        verbose_name = "Precios"
        verbose_name_plural = "Precios"

class ElementPriceAdminPanel(admin.ModelAdmin):
    #Panel de admin
    list_display = ('buyExerciseValue' , 'promoteExerciseValue')

