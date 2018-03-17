from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.
from licenseTypes.models import LicenseType


class License(models.Model):
    # Atributos de la clase LicenseType: numUsers, numFreeExercises, price, startDate, endDate
    numUsers = models.PositiveIntegerField(default=0)
    numFreeExercises = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)

    #Relación ManyToOne con LicenseType
    licenseType = models.ForeignKey(LicenseType, on_delete=models.CASCADE, null=True)
    #Relación ManyToOne con School
    #school = models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self):
        return self.numUsers + ' - ' + self.numFreeExercises + ' - ' + self.price + ' ( ' + self.startDate + ' -- ' + self.endDate + ' ) '

    class Meta:
        verbose_name_plural = "Licenses"


class LicenseAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('numUsers', 'numFreeExercises', 'price', 'startDate', 'endDate')

