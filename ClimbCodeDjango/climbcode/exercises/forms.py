from django import forms


class BuyExerciseForm(forms.Form):

    exerciseId = forms.IntegerField()
    freePurchase = forms.BooleanField()
