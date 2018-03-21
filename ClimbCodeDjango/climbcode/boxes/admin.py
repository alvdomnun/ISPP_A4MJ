from django.contrib import admin
from boxes.models import Box, BoxAdminPanel, Parameter, ParameterAdminPanel, Picture, PictureAdminPanel, Text, TextAdminPanel, Code, CodeAdminPanel

# Register your models here.
admin.site.register(Box, BoxAdminPanel)
admin.site.register(Text, TextAdminPanel)
admin.site.register(Code, CodeAdminPanel)
admin.site.register(Picture, PictureAdminPanel)
admin.site.register(Parameter, ParameterAdminPanel)