from django.contrib import admin
from elementPrices.models import ElementPrice, ElementPriceAdminPanel

# Register your models here.
admin.site.register(ElementPrice, ElementPriceAdminPanel)