from django.core.validators import MinValueValidator
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.
from exercises.models import Exercise


class Box(models.Model):
    # Atributos de la clase Box: order
    order = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)] )


    #Relación ManyToOne con Exercise
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.order

    class Meta:
        verbose_name_plural = "Boxes"


class BoxAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('order',)


#Box -> Text

class Text(Box):
    #Clase que define a Text
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Texts"


class TextAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('order', 'title', 'exercise')



class Code(Box):
    #Clase que define a Text
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Codes"


class CodeAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('order', 'title', 'exercise')


class Picture(Box):
    #Clase que define a Text
    def __str__(self):
        return '( ' + self.order + ' ) ' + self.exercise.title

    class Meta:
        verbose_name_plural = "Pictures"


class PictureAdminPanel(admin.ModelAdmin):
    """
    Clase que define las propiedades del Administrador que se mostrarán en el panel de administración.
    """
    list_display = ('order', 'title', 'exercise')
