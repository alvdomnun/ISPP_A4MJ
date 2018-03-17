from django.contrib import admin
from licenses.models import License, LicenseAdminPanel

# Register your models here.
admin.site.register(License, LicenseAdminPanel)