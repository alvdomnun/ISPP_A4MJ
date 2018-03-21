from django.contrib import admin
from provinces.models import Province, ProvinceAdminPanel

# Register your models here.
admin.site.register(Province, ProvinceAdminPanel)