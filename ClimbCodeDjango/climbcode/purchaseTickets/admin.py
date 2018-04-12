from django.contrib import admin
from purchaseTickets.models import PurchaseTicket, PurchaseTicketAdminPanel

# Register your models here.
admin.site.register(PurchaseTicket, PurchaseTicketAdminPanel)