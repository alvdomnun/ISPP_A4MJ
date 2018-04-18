from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from defaultSubjects.models import DefaultSubject


class Exercise(models.Model):
    #Atributos de la clase Exercise: title, description, level, sales, promoted, startPromotionDate, endPromotionDate, daft, subjectCategory

    #Tipos de nivel
    EASY = 'Fácil'
    MEDIUM = 'Medio'
    HARD = 'Difícil'
    LevelType = (
        (EASY, 'Fácil'),
        (MEDIUM, 'Medio'),
        (HARD, 'Difícil')
    )

    title = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    description = models.TextField()
    sales = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=10, choices=LevelType, default=EASY)
    promoted = models.BooleanField()
    startPromotionDate = models.DateField(null=True, blank=True)
    endPromotionDate = models.DateField(null=True, blank=True)
    draft = models.BooleanField(default=True)

    # Relación con DefaultSubject = Categoría (las asignaturas que incluye el sistema por defecto)
    category = models.ForeignKey(DefaultSubject, on_delete=models.CASCADE, null=True)
    # Relación con Programador
    programmer = models.ForeignKey('actors.Programmer', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.title) + ' - ' + str(self.sales)  + ' - ' + str(self.level) + ' ( ' + str(self.promoted) + ' - ' + str(self.draft) + ' )'

    class Meta:
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"


class ExerciseAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'level', 'promoted', 'sales', 'draft', 'get_default_subject')

    def get_default_subject(self, obj):
        return obj.category.name + ' ' + str(obj.category.course)
