from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from actors.models import Teacher
from subjects.models import Subject


class EditTeacherForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    # Validaciones adicionales
    #def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden

class EditStudentForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')
    subjects = forms.ModelMultipleChoiceField(queryset = Subject.objects.all(), label = 'Asignaturas')

    # Validaciones adicionales
    #def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden



class RegisterTeacherForm(forms.Form):
    # Atributos de información personal
    username = forms.CharField(min_length=5, max_length=32, label='Nombre de usuario')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    # Validaciones adicionales
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username=username).count()
            if (num_usuarios > 0):
                raise forms.ValidationError(
                    "El nombre de usuario ya está ocupado. Por favor, eliga otro para completar su registro.")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")


class RegisterStudentForm(forms.Form):
    # Atributos de información personal
    username = forms.CharField(min_length=5, max_length=32, label='Nombre de usuario')
    password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar contraseña')
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length=11, validators=[RegexValidator(regex=r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$')],
                            label='Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')
    subjects = forms.ModelMultipleChoiceField(queryset = Subject.objects.all(), label = 'Asignaturas')

    # Validaciones adicionales
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el username no sea repetido
            username = self.cleaned_data["username"]
            num_usuarios = User.objects.filter(username=username).count()
            if (num_usuarios > 0):
                raise forms.ValidationError(
                    "El nombre de usuario ya está ocupado. Por favor, eliga otro para completar su registro.")

            # Valida que la contraseña se haya confirmado correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                raise forms.ValidationError(
                    "Las contraseñas introducidas no coinciden. Por favor, asegúrese de confirmarla correctamente.")
