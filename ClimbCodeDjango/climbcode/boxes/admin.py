from django.contrib import admin
from boxes.models import Box, BoxAdminPanel, Parameter, ParameterAdminPanel

# Register your models here.
admin.site.register(Box, BoxAdminPanel)
admin.site.register(Parameter,ParameterAdminPanel)