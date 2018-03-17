from django.contrib import admin
from parameters.models import Parameter, ParameterAdminPanel

# Register your models here.
admin.site.register(Parameter,ParameterAdminPanel)