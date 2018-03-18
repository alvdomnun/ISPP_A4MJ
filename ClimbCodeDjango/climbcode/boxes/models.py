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
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Texts"


class TextAdminPanel(BoxAdminPanel):
    pass


class Code(Box):
    # Clase que define a Text
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Codes"


class CodeAdminPanel(BoxAdminPanel):
    pass


class Picture(Box):
    #Clase que define a Text
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Pictures"


class PictureAdminPanel(BoxAdminPanel):
    pass


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