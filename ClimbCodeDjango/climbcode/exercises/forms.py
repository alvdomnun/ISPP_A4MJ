from django import forms


class BuyExerciseForm(forms.Form):
    """ Formulario para recibir el pago de Paypal cuando se compra un ejercicio """

    exerciseId = forms.IntegerField()
    payment = forms.IntegerField()
    freePurchase = forms.IntegerField()

class PromoteExerciseForm(forms.Form):
    """ Formulario para recibir el pago de Paypal cuando se promociona un ejercicio """

    exerciseId = forms.IntegerField()
    payment = forms.IntegerField()
