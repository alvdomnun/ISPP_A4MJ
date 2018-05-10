"""
Definition of forms.
"""
#encoding:utf-8

from django import forms
from licenses.models import License
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import RegexValidator
from provinces.models import Province
from actors.models import School, validate
from licenses.models import LicenseType
import re
from django.forms import ModelForm
from exercises.models import Exercise
from defaultSubjects.models import DefaultSubject

class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    username = forms.CharField(max_length=254, widget=forms.TextInput({'class': 'form-control', 'required': True, 'autofocus': True, 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label=_("Contraseña"), widget=forms.PasswordInput({'class': 'form-control', 'required': True, 'placeholder':'Contraseña'}))


class RegisterProgrammerForm(forms.Form):
    """Formulario registro como Programador"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length = 5, max_length = 32, label = 'Nombre de usuario')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Programador
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    dni = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$',
                message = 'El D.N.I. debe estar compuesto de 8 dígitos seguidos de 1 letra mayúscula.')], label = 'D.N.I.')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username = username).count()
            if (num_usuarios > 0):
                    raise forms.ValidationError("El nombre de usuario ya está ocupado. Por favor, eliga otro para completar su registro.")

            dni = self.cleaned_data["dni"]
            try:
                validate(dni)
            except Exception as e:
                raise forms.ValidationError("El formato del DNI no es correcto")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")


      
class RegisterSchoolForm(forms.Form):
    """Formulario registro como Escuela"""

    # Campos requeridos por el User model
    username = forms.CharField(min_length = 5, max_length = 32, label = 'Nombre de usuario')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Escuela
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{9})$', 
           message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required = False, label = 'Foto de perfil')
    centerName = forms.CharField(max_length = 50, label = 'Nombre del Centro')
    address = forms.CharField(max_length = 50, label = 'Dirección')
    postalCode = forms.CharField(max_length = 5, validators = [RegexValidator(regex = r'^(\d{5})$')], label = 'Código Postal')
    province = forms.ModelChoiceField(queryset = Province.objects.all(), empty_label = None, label = 'Provincia')
    type = forms.ChoiceField(choices = School.SchoolType, label = 'Tipo Escuela')
    teachingType = forms.ChoiceField(choices = School.TeachingType, label = 'Enseñanza')
    identificationCode = forms.CharField(max_length = 9, label = 'Código de identificación')
    licenseType = forms.ModelChoiceField(queryset = LicenseType.objects.all(), empty_label = None, label = 'Licencia')
    numUsers = forms.IntegerField(required = False, label = 'Número de usuarios')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username = username).count()
            if (num_usuarios > 0):
                # Busca el usuario por username
                user = User.objects.filter(username = username)
                # Si es programador o es una escuela ya activada, error de username ocupado
                if (hasattr(user[0].actor, 'programmer')) or (hasattr(user[0].actor, 'school') and user[0].actor.school.isPayed):
                    raise forms.ValidationError("El nombre de usuario ya está ocupado. Por favor, elija otro para completar su registro.")

            school_code = self.cleaned_data["identificationCode"]
            num_codigo = School.objects.filter(identificationCode=school_code).exclude(isPayed=False).count()
            if (num_codigo > 0):
                raise forms.ValidationError(
                    "El código de identificación que ha ingresado ya está siendo utilizado por otro instituto o academia")

            dni = self.cleaned_data["dni"]
            try:
                validate(dni)
            except Exception as e:
                raise forms.ValidationError("El formato del DNI no es correcto")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")

            # Valida los patrones para cuando sea escuela o academia
            type = self.cleaned_data["type"]
            idCode = self.cleaned_data["identificationCode"]
            if idCode is not None and type == 'Instituto':
                if re.match(r'^(\d{8})$', idCode) is None:
                    raise forms.ValidationError('El código de identificación de un instituto se compone de 8 dígitos.')
            elif idCode is not None and type == 'Academia':
                if re.match(r'^(\d{9})$', idCode) is None:
                    raise forms.ValidationError('El código de identificación de una academia se compone de 9 dígitos.')

            # Valida que el número de usuarios indicados no sea inferior al de la licencia dada
            licenseType = self.cleaned_data["licenseType"]
            license = LicenseType.objects.filter(pk = licenseType.id)[0]
            numUsers = self.cleaned_data["numUsers"]
             # Valida que el número de usuarios solicitado sea mayor que el mínimo exigido por la licencia
            if (license.numUsers > numUsers):
                raise forms.ValidationError("El número de usuarios indicado no supera el mínimo exigido por la licencia.")

class ExerciseForm(forms.Form):
    """
    Formulario para el modelo Exercise
    """
    title = forms.CharField()
    description = forms.CharField()
    level = forms.ChoiceField(choices = Exercise.LevelType, label = 'Nivel')
    category = forms.ModelChoiceField(queryset = DefaultSubject.objects.all(), empty_label = None, label = 'Asignatura')

class RegisterSchoolPaymentForm(forms.Form):
    """ Formulario para recibir el pago de Paypal """

    license = forms.IntegerField();
    licensePrice = forms.CharField(min_length = 6, max_length = 10);
    payment = forms.IntegerField();
    school = forms.IntegerField();

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el usuario de la escuela esté inactivo
            school = self.cleaned_data["school"]
            school = School.objects.filter(pk = school).first()
            if (school.userAccount.is_active):
                raise forms.ValidationError("Esta escuela ya está activa.")

            # Valida que la licencia que se paga corresponda con la escuela
            license = self.cleaned_data["license"]
            license = License.objects.filter(id = license).first()
            if not(license.school == school):
                raise forms.ValidationError("La licencia que se intenta pagar no pertenece a la escuela.")

            # Valida el precio de licencia que trae el form sea similar al de la licencia
            licensePrice = self.cleaned_data["licensePrice"]
            # Formatea cambiando la coma del decimal por punto (, -> .)
            licensePrice = licensePrice.replace(',', '.')
            if not(licensePrice == str(license.price)):
                raise forms.ValidationError('El precio de la licencia no corresponde con el real.')
