from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms.utils import ErrorList

from actors.models import Teacher, School
from subjects.models import Subject
from _datetime import date
import datetime

class EditSelfTeacherForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')


class EditSelfTeacherPassForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.password = kwargs.pop('password')
        super(EditSelfTeacherPassForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(required=False, initial=self.password)


    actual_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput, label='Contraseña actual')
    new_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Nueva contraseña')
    confirm_new_password = forms.CharField(min_length=5, max_length=32, widget=forms.PasswordInput,
                                       label='Confirmar nueva contraseña')
    email = forms.HiddenInput
    first_name = forms.HiddenInput
    last_name = forms.HiddenInput

    # Atributos propios de la clase
    phone = forms.HiddenInput
    photo = forms.HiddenInput
    dni = forms.HiddenInput

    # Validaciones adicionales
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            actual_password = self.cleaned_data['actual_password']
            if not self.user.check_password(actual_password):
                raise forms.ValidationError(
                    "La contraseña actual no es correcta. Por favor, asegúrese de confirmarla correctamente.")

            new_password = self.cleaned_data['new_password']
            confirm_new_password = self.cleaned_data['confirm_new_password']
            if new_password != confirm_new_password:
                raise forms.ValidationError(
                    "La nuevas contraseñas no coinciden. Por favor, asegúrese de confirmarlas correctamente.")

            if new_password == actual_password:
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")

class EditTeacherForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
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
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')
    #subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.none())

# Validaciones adicionales
    #def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden


def get_license_school(school):
    """ Obtiene la licencia activa para la escuela indicada """

    # Fecha actual
    today = datetime.date.today()

    # Obtiene la licencia de la escuela cuya fecha de finalización supere a la actual (es decir, aquella activa)
    license = school.license_set.filter(endDate__gte = today)

    # Si se encuentra licencia activa, la devuelve
    if (license.count() > 0):
        return license.first()

    # Si no se encuentra
    else:
        False

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
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.none())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterTeacherForm, self).__init__(*args, **kwargs)
        self.fields['subjects'] = forms.ModelMultipleChoiceField(
            queryset=Subject.objects.filter(school__userAccount_id=self.user.id), label='Asignaturas')

    # Validaciones adicionales
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Comprueba que la licencia activa de la escuela no tenga el contador de usuarios a añadir a 0
            school = School.objects.get(userAccount_id=self.user.id)
            license = get_license_school(school)
            if not license:
                raise forms.ValidationError(
                    "No tienen ninguna licencia activa. Diríjase al apartado de compra de licencias.")
            else:
                if license.numUsers == 0:
                    raise forms.ValidationError(
                        "Su licencia no permite el registro de más usuarios.")


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
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.none())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterStudentForm, self).__init__(*args, **kwargs)
        self.fields['subjects'] = forms.ModelMultipleChoiceField(queryset = Subject.objects.filter(school__userAccount_id=self.user.id), label = 'Asignaturas')


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


class EditProgrammerProfile(forms.Form):
    """ Formulario de edición del perfil Programador """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Programador
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    dni = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], label = 'D.N.I.')


class EditProgrammerPass(forms.Form):
    """ Formulario de edición de las contraseñas del usuario """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")


class EditSchoolProfile(forms.Form):
    """ Formulario de edición del perfil Student """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')
    # Campos requeridos por el modelo Actor-Student
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    centerName = forms.CharField(max_length=50, required=False, label='Nombre del centro')
    address = forms.CharField(max_length=50, required=False, label='Dirección' )
    identificationCode = forms.CharField( max_length = 9, required=False, label = 'CIF o código del centro')
    postalCode = forms.CharField( max_length = 5, validators = [RegexValidator(regex = r'^(\d{5})$')], label='Código postal')

class EditSchoolPass(forms.Form):
    """ Formulario de edición de las contraseñas del usuario """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")

class EditStudentProfile(forms.Form):
    """ Formulario de edición del perfil Student """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Student
    phone = forms.CharField(max_length = 11, validators = [RegexValidator(regex = r'^(\d{3})(\-)(\d{3})(\-)(\d{3})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos siguiendo el patrón: XXX-XXX-XXX.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    dni = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], label = 'D.N.I.')


class EditStudentPass(forms.Form):
    """ Formulario de edición de las contraseñas del usuario """
    userAccountId = forms.IntegerField()
    actual_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Contraseña actual')
    password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Nueva contraseña')
    confirm_password = forms.CharField(min_length = 5, max_length = 32, widget = forms.PasswordInput, label = 'Confirmar nueva contraseña')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida la contraseña actual del usuario sea la que ha introducido en el formulario
            actual_password = self.cleaned_data["actual_password"]
            userAccountId = self.cleaned_data["userAccountId"]
            userAccount = User.objects.get(pk = userAccountId)
            if not (userAccount.check_password(actual_password)):
                    raise forms.ValidationError("Por favor, introduzca correctamente su contraseña actual para realizar el cambio.")

            # Valida que la nueva contraseña haya sido confirmada correctamente
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["confirm_password"]
            if (password != confirm_password):
                    raise forms.ValidationError("La nueva contraseña no coincide. Por favor, asegúrese de confirmarla correctamente.")

            # Valida que la nueva contraseña no sea igual a la actual
            if (password == actual_password):
                raise forms.ValidationError("La nueva contraseña no puede ser similar a la actual. Por favor, elija otra.")
