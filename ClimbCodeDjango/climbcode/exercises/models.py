from django.db import models
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Create your models here.
from defaultSubjects.models import DefaultSubject


class Exercise(models.Model):
    #Atributos de la clase Exercise: title, description, level, sales, promoted, startPromotionDate, endPromotionDate, daft, subjectCategory

    #Tipos de nivel
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    LevelType = (
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard')
    )

    title = models.CharField(max_length=50, help_text="Requerido. 50 carácteres como máximo")
    description = models.TextField()
    sales = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=10, choices=LevelType, default=EASY)
    promoted = models.BooleanField()
    startPromotionDate = models.DateField(null=True, blank=True)
    endPromotionDate = models.DateField(null=True, blank=True)
    draft = models.BooleanField(default=True)
    #subjectCategory
    #subjectCategory = models.ForeignKey(DefaultSubject,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title + ' - ' + self.description + ' - ' + self.sales  + ' - ' \
               + self.level + ' ( ' + self.promoted + ' : ' + self.startPromotionDate + ' -- '+ self.endPromotionDate + ' )  ' + self.draft

    class Meta:
        verbose_name_plural = "Exercises"


class ExerciseAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('title', 'description', 'sales', 'level', 'promoted', 'startPromotionDate', 'endPromotionDate', 'draft')


