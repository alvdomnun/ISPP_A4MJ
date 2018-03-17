from django.contrib import admin
from defaultSubjects.models import DefaultSubject, DefaultSubjectAdminPanel

# Register your models here.
admin.site.register(DefaultSubject, DefaultSubjectAdminPanel)