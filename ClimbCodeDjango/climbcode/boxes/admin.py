from django.contrib import admin
from boxes.models import Box, BoxAdminPanel

# Register your models here.
admin.site.register(Box, BoxAdminPanel)