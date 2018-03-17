from django.contrib import admin
from exercises.models import Exercise, ExerciseAdminPanel

# Register your models here.
admin.site.register(Exercise, ExerciseAdminPanel)