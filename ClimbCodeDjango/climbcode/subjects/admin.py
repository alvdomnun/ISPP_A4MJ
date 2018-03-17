from django.contrib import admin
from subjects.models import Subject, SubjectAdminPanel

# Register your models here.
admin.site.register(Subject, SubjectAdminPanel)