import re

from django import forms
from licenses.models import License
from licenses.models import LicenseType
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms.utils import ErrorList
from actors.models import Teacher, School
from _datetime import date
import datetime

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UploadFileForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.errors:

            file_obj = self.cleaned_data.get('file')

            data = file_obj.read().decode('utf-8')

            rows = re.split('\n', data)

            school = School.objects.get(userAccount_id=self.user.id)
            license = get_license_school(school)
            if not license:
                raise forms.ValidationError(
                    "No tienen ninguna licencia activa. Diríjase al apartado de compra de licencias.")
            else:
                if license.numUsers == 0:
                    raise forms.ValidationError(
                        "Su licencia no permite el registro de más usuarios.")

                if rows.__len__() > license.numUsers:
                    raise forms.ValidationError(
                        "El número de estudiantes que estás intenando añadir es superior a los restantes de tu licencia")


class EditTeacherForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

class EditStudentForm(forms.Form):
    # Atributos de información personal
    username = forms.HiddenInput
    password = forms.HiddenInput
    confirm_password = forms.HiddenInput
    email = forms.EmailField()
    first_name = forms.CharField(min_length=2, max_length=32, label='Nombre')
    last_name = forms.CharField(min_length=2, max_length=50, label='Apellidos')

    # Atributos propios de la clase
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

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
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterTeacherForm, self).__init__(*args, **kwargs)

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
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required=False)
    dni = forms.CharField(max_length=9, validators=[RegexValidator(regex=r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')],
                          label='D.N.I.')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterStudentForm, self).__init__(*args, **kwargs)

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

class EditProgrammerProfile(forms.Form):
    """ Formulario de edición del perfil Programador """

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Programador
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
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
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    centerName = forms.CharField(max_length=50, label='Nombre del centro')
    address = forms.CharField(max_length=50, label='Dirección' )
    identificationCode = forms.CharField( max_length = 9, validators = [RegexValidator(regex = r'^(\d{8,9})$',
           message = 'El código de identificación debe estar compuesto de 8 dígitos o 9 dígitos.')],label = 'CIF o código del centro')
    postalCode = forms.CharField( max_length = 5, validators = [RegexValidator(regex = r'^(\d{5})$')], label='Código postal')

    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            school_code = self.cleaned_data["identificationCode"]
            num_codigo = School.objects.filter(identificationCode=school_code).exclude(isPayed=False).count()
            if (num_codigo > 0):
                raise forms.ValidationError(
                    "El código de identificación que ha ingresado ya está siendo utilizado por otro instituto o academia")

            # Valida los patrones para cuando sea escuela o academia
            type = self.cleaned_data["type"]
            idCode = self.cleaned_data["identificationCode"]
            if idCode is not None and type == 'Instituto':
                if re.match(r'^(\d{8})$', idCode) is None:
                    raise forms.ValidationError('El código de identificación de un instituto se compone de 8 dígitos.')
            elif idCode is not None and type == 'Academia':
                if re.match(r'^(\d{9})$', idCode) is None:
                    raise forms.ValidationError('El código de identificación de una academia se compone de 9 dígitos.')

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
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
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

class EditTeacherProfile(forms.Form):

    # Campos editables del User model
    email = forms.EmailField()
    first_name = forms.CharField(min_length = 2, max_length = 32, label = 'Nombre')
    last_name = forms.CharField(min_length = 2, max_length = 50, label = 'Apellidos')

    # Campos requeridos por el modelo Actor-Student
    phone = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^(\d{9})$',
                message = 'El teléfono debe estar compuesto de 9 dígitos.')], label = 'Teléfono')
    photo = forms.ImageField(required = False)
    dni = forms.CharField(max_length = 9, validators = [RegexValidator(regex = r'^([0-9]{8})([TRWAGMYFPDXBNJZSQVHLCKE])$')], label = 'D.N.I.')

class EditTeacherPass(forms.Form):
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


class RenovateLicenseForm(forms.Form):
    """Formulario de renovación de licencia"""

    # Campos requeridos por el modelo Actor-Escuela
    licenseType = forms.ModelChoiceField(queryset = LicenseType.objects.all(), empty_label = None, label = 'Licencia')
    numUsers = forms.IntegerField(required = False, label = 'Número de usuarios')

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el número de usuarios indicados no sea inferior al de la licencia dada
            licenseType = self.cleaned_data["licenseType"]
            license = LicenseType.objects.filter(pk = licenseType.id)[0]
            numUsers = self.cleaned_data["numUsers"]
             # Valida que el número de usuarios solicitado sea mayor que el mínimo exigido por la licencia
            if (license.numUsers > numUsers):
                raise forms.ValidationError("El número de usuarios indicado no supera el mínimo exigido por la licencia.")

class RenovateLicensePaymentForm(forms.Form):
    """ Formulario para recibir el pago de Paypal """

    license = forms.IntegerField();
    licensePrice = forms.CharField(min_length = 6, max_length = 10);
    payment = forms.IntegerField();
    school = forms.IntegerField();

    # Validaciones propias
    def clean(self):
        # Si no se han capturado otros errores, hace las validaciones por orden
        if not self.errors:

            # Valida que el usuario de la escuela no tenga licencia activa
            school = self.cleaned_data["school"]
            school = School.objects.filter(pk = school).first()
            today = datetime.date.today()
            license = school.license_set.filter(endDate__gte = today)
            if (license.count() > 0):
                raise forms.ValidationError("Esta escuela ya dispone de licencia activa.")

            # Valida que la licencia que se paga corresponda con la escuela
            license = self.cleaned_data["license"]
            license = License.objects.filter(id = license).first()
            if not(license.school == school):
                raise forms.ValidationError("La licencia que se intenta pagar no pertenece a la escuela.")
            # Valida que la licencia no tenga fecha de fin actia
            if license.endDate is not None:
                raise forms.ValidationError("La licencia que se intenta pagar ya está activa.")

            # Valida el precio de licencia que trae el form sea similar al de la licencia
            licensePrice = self.cleaned_data["licensePrice"]
            # Formatea cambiando la coma del decimal por punto (, -> .)
            licensePrice = licensePrice.replace(',', '.')
            if not(licensePrice == str(license.price)):
                raise forms.ValidationError('El precio de la licencia no corresponde con el real.')

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