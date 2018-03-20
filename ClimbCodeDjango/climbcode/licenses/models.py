from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from actors.models import School
from django.core.validators import RegexValidator



class License(models.Model):
    # Atributos de la clase LicenseType: numUsers, numFreeExercises, price, startDate, endDate

    numUsers = models.PositiveIntegerField(default=0)
    numFreeExercises = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)

    #Relación ManyToOne con LicenseType: on_delete=models.SET_NULL (si se elimina la licencia básica: FK = Null)
    licenseType = models.ForeignKey('LicenseType', on_delete=models.SET_NULL, null=True)
    #Relación ManyToOne con School
    school = models.ForeignKey(School, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.numUsers + ' - ' + self.numFreeExercises + ' - ' + self.price + ' ( ' + self.startDate + ' -- ' + self.endDate + ' ) '

    class Meta:
        verbose_name = "Licencia"
        verbose_name_plural = "Licencias"


class LicenseAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('get_school', 'numUsers', 'numFreeExercises', 'price', 'startDate', 'endDate')

    def get_school(self, obj):
        return obj.school.name


class LicenseType(models.Model):
    #Atributos de la clase LicenseType: name, numUsers, numFreeExercises, price

    name =models.CharField(max_length = 50, help_text = 'Requerido. 50 carácteres como máximo.',default= 'BASIC',
        validators = [RegexValidator(regex = r'^BASIC$' or '^MEDIUM$' or r'^LARGE$' , message = 'El formato introducido es incorrecto. Debe ser BASIC, MEDIUM, LARGE')])
    numUsers = models.PositiveIntegerField(default=0)
    numFreeExercises = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default = 0.0, max_digits = 9, decimal_places = 2)

    #Sin relaciones

    def __str__(self):
        return self.name + ' - ' + self.numUsers + ' - ' + self.numFreeExercises + ' -- ' + self.price

    class Meta:
        verbose_name = "Licencia Tipo"
        verbose_name_plural = "Licencias Tipo"


class LicenseTypeAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('name', 'numUsers','numFreeExercises', 'price')

