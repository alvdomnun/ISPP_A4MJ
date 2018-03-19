"""
Definition of forms.
"""
#encoding:utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    username = forms.CharField(max_length=254, widget=forms.TextInput({'class': 'form-control', 'required': True, 'autofocus': True, 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput({'class': 'form-control', 'required': True, 'placeholder':'Contraseña'}))
