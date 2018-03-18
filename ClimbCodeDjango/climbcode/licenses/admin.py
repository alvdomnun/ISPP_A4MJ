from django.contrib import admin
from licenses.models import License, LicenseAdminPanel, LicenseType, LicenseTypeAdminPanel

# Register your models here.
admin.site.register(License, LicenseAdminPanel)
admin.site.register(LicenseType, LicenseTypeAdminPanel)