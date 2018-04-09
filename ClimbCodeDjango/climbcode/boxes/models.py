from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from exercises.models import Exercise


class Box(models.Model):
    # Atributos de la clase Box: order
    order = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)] )


    # Relación ManyToOne con Exercise
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order

    class Meta:
        verbose_name_plural = "Boxes"


class BoxAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('order', 'get_exercise', 'get_category')

    def get_exercise(self, obj):
        return obj.exercise.title

    def get_category(self, obj):
        return obj.exercise.category.name


class Text(Box):
    #Clase que define a Text
    content = models.TextField(default="")

    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name = "Texto"
        verbose_name_plural = "Textos"


class TextAdminPanel(BoxAdminPanel):
    pass


class Code(Box):
    # Clase que define a Text
    content = models.TextField(default="")

    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name = "Código"
        verbose_name_plural = "Códigos"


class CodeAdminPanel(BoxAdminPanel):
    pass


class Picture(Box):
    #Clase que define a Text
    content = models.ImageField(upload_to = 'uploads/',default=None)

    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name = "Gráfica"
        verbose_name_plural = "Gráficas"

class PictureAdminPanel(BoxAdminPanel):
    pass


class Parameter(models.Model):
    # Atributos de la clase Parameter: id
    value = models.TextField(default="")
    idName = models.TextField(default="")

    #Relación ManyToOne con Code
    code = models.ForeignKey('boxes.Code', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Parámetro"
        verbose_name_plural = "Parámetros"


class ParameterAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('id',)