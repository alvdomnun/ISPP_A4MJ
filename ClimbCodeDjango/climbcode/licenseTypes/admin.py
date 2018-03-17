from django.contrib import admin
from licenseTypes.models import LicenseType, LicenseTypeAdminPanel

# Register your models here.
admin.site.register(LicenseType, LicenseTypeAdminPanel)