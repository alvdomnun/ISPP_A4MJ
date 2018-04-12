from django.db import models
from actors.models import School
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from exercises.models import Exercise

# Create your models here.

class PurchaseTicket(models.Model):
    # Atributos de la clase PurchaseTicket: date, paymentMethod, price, 

    # Tipos de pago
    PAYPAL = 'Paypal'
    FREE = 'Free'
    PaymentMethod = (
        (PAYPAL, 'Paypal'),
        (FREE, 'Free')
    )

    date = models.DateField(verbose_name = 'Fecha de compra', auto_now = True)
    price = models.DecimalField(verbose_name = 'Precio de compra', default=0.0, max_digits=9, decimal_places=2)
    paymentMethod = models.CharField(verbose_name = 'Tipo de Pago', max_length = 20, choices = PaymentMethod, default = PAYPAL)

    # Relación con School
    school = models.ForeignKey(School, on_delete=models.CASCADE, null = True)
    # Relación con Exercise: on_delete=models.SET_NULL (si se elimina el ejercicio: FK = Null)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.price) + ' - ' + self.paymentMethod + ' - ' + str(self.date)

    class Meta:
        verbose_name = "Ticket de Compra"
        verbose_name_plural = "Tickets de Compra"


class PurchaseTicketAdminPanel(admin.ModelAdmin):
    # Panel de admin
    list_display = ('date', 'price', 'get_user_school', 'get_school', 'get_exercise')

    def get_user_school(self, obj):
        return obj.school.userAccount.get_username()

    def get_school(self, obj):
        return obj.school.centerName

    def get_exercise(self, obj):
        return obj.exercise.title