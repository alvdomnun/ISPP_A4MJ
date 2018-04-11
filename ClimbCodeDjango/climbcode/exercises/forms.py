from django import forms


class BuyExerciseForm(forms.Form):
    """ Formulario para recibir el pago de Paypal """

    exerciseId = forms.IntegerField()
    payment = forms.IntegerField()
    freePurchase = forms.IntegerField()
