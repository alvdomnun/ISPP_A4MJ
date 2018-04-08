from django.shortcuts import render, render_to_response
from web.forms import RegisterSchoolPaymentForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date
from web.forms import RegisterProgrammerForm, RegisterSchoolForm
from django.contrib.auth.models import User
from actors.models import School, Programmer
from licenses.models import LicenseType, License
from provinces.models import Province


# Create your views here.

def index(request):
	template = loader.get_template('welcome/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def web_index(request):
	template = loader.get_template('web/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def sample_dashboard(request):
	template = loader.get_template('samples/sampleDashboard.html')
	context = {}
	return HttpResponse(template.render(context,request))

def notebookVistaV1(request):
	template = loader.get_template('notebook/notebookVistaV1.html')
	context = {}
	return HttpResponse(template.render(context,request))

def notebookv1(request):
	template = loader.get_template('web/notebookv1.html')
	context = {}
	return HttpResponse(template.render(context, request))

def notebookv1aux(request):
	template = loader.get_template('web/notebookv1aux.html')
	context = {}
	return HttpResponse(template.render(context, request))

def notebookv1_ejercicio_creado(request):
    template = loader.get_template('web/notebookv1_ejercicio_creado.html')
    context = {}
    return HttpResponse(template.render(context, request))

def notebookv1_ejercicio_cc(request):
    template = loader.get_template('web/notebookv1_ejercicio_cc.html')
    context = {}
    return HttpResponse(template.render(context, request))

def notebookv1_ejercicio_am(request):
    template = loader.get_template('web/notebookv1_ejercicio_am.html')
    context = {}
    return HttpResponse(template.render(context, request))

def notebookv1_ejercicio_qin(request):
    template = loader.get_template('web/notebookv1_ejercicio_qin.html')
    context = {}
    return HttpResponse(template.render(context, request))

def notebookv1_ejercicio_est(request):
    template = loader.get_template('web/notebookv1_ejercicio_est.html')
    context = {}
    return HttpResponse(template.render(context, request))

def register_programmer(request):
    """
	Registro del Programador en el sistema.
	"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterProgrammerForm(request.POST)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]              

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Crea el Programador y lo asocia al User anterior
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]
            userAccount = user

            programmer = Programmer.objects.create(phone = phone, photo = photo, dni = dni, userAccount = userAccount)

            return HttpResponseRedirect('/login/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterProgrammerForm()
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'title': 'Registro de Programador',
        'year': datetime.now().year,
    }
        
    return render(request, 'web/registerProgrammer.html', data)

def register_school(request):
    """
	Registro de la Escuela en el sistema.
	"""
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterSchoolForm(request.POST)
        if (form.is_valid()):
            # Objeto User (model Django)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]            
            
            # Licencia Tipo
            licenseType = form.cleaned_data["licenseType"]
            # Crear la licencia específica en funcion de la licencia tipo (licenseType) y si ha añadido usuarios extras
            licenseType = LicenseType.objects.filter(id = licenseType.id)[0]
            licenseNumUsers = form.cleaned_data["numUsers"]
            licensePrice = getFinalPrice(licenseType, licenseNumUsers)

            # Escuela
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            province = form.cleaned_data["province"]
            address = form.cleaned_data["address"]
            postalCode = form.cleaned_data["postalCode"]
            centerName = form.cleaned_data["centerName"]
            type = form.cleaned_data["type"]
            teachingType = form.cleaned_data["teachingType"]
            identificationCode = form.cleaned_data["identificationCode"]

            # Persiste el User Model (inactivo hasta el pago con Paypal)
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            #TODO : De momento se crean inactivos -> Habrá que activarlo tras el pago de Paypal
            user.is_active = False
            user.save()

            # Asocia el Usuario a la escuela y la persiste
            userAccount = user
            school = School.objects.create(phone = phone, photo = photo, province = province, address = address, type = type, teachingType = teachingType, 
                centerName = centerName, postalCode = postalCode, identificationCode = identificationCode, userAccount = userAccount)

            # Crea las fechas de la licencia
            today = date.today()
            endDate = date(today.year + 1, today.month, today.day)
            # Guarda la licencia asociándola a la escuela que se registra
            license = License.objects.create(numUsers = licenseNumUsers, price = licensePrice, numFreeExercises = licenseType.numFreeExercises,
                endDate = endDate, licenseType = licenseType, school = school)

            paymentData = {
                'school': school,
                'license': license,
                'date': date.today()
            }

            return render(request, 'web/registerPayment.html', paymentData)

        else:
            # Si la validación falla también cargo los datos necesarios
            provinces = Province.objects.all()
            licenses = LicenseType.objects.all()
            types = form.fields['type'].choices
            teachingTypes = form.fields['teachingType'].choices

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterSchoolForm()

        # Datos del modelo (vista)
        provinces = Province.objects.all()
        licenses = LicenseType.objects.all()
        types = form.fields['type'].choices
        teachingTypes = form.fields['teachingType'].choices
    
    data = {
        'form': form,
        'provinces': provinces,
        'licenseTypes': licenses,
        'schoolTypes': types,
        'teachingTypes': teachingTypes,
        'title': 'Registro de Escuela',
        'year': datetime.now().year,
    }

    return render(request, 'web/registerSchool.html', data)

def paypalTransaction(request):
    """
        Controla el pago del usuario tras 
    """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseForbidden()

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RegisterSchoolPaymentForm(request.POST)
        if (form.is_valid()):
            # Extrae valores y activa el usuario si el pago ha sido correcto
            school = form.cleaned_data["school"]
            license = form.cleaned_data["license"]
            licensePrice = form.cleaned_data["licensePrice"]
            payment = form.cleaned_data["payment"]

            # Obtiene la licencia y la escuela a partir de los Ids que trae el form
            school = School.objects.filter(pk = school).first()
            license = License.objects.filter(id = license).first()

            # Si el pago se ha ejecutado correctamente, se activa la escuela
            if (payment == 1):
                school.userAccount.is_active = True
                school.userAccount.save()

                return HttpResponseRedirect('/login/')

            # Si el pago no ha sido correcto (payment == 0), recarga la página para que vuelva a intentar el pago
            else:
                paymentData = {
                    'school': school,
                    'license': license,
                    'date': date.today()
                }

                return render(request, 'web/registerPayment.html', paymentData)
        else:
            # Si el form no es válido, Forbidden
            return HttpResponseForbidden()
    
    # Si el request no es un POST con el pago, Forbidden
    return HttpResponseForbidden()


####################################################    PRIVATE     METHODS     #################################################################

def getFinalPrice(license, numUsers):
    """
    Calcula el precio final de la licencia a partir del tipo básico y el número de usuarios final
    """

    # Valida que el número de usuarios solicitado sea mayor que el mínimo exigido por la licencia
    if (license.numUsers > numUsers):
        return HttpResponseForbidden()

    # Precio unitario de cada usuario extra para la licencia escogida
    unitPricePerUser = round((license.price / license.numUsers), 2)
    # Número de usuarios extras añadidos
    extraUsers = numUsers - license.numUsers

    # Precio final = Precio por defecto + (Nº Usuarios Extra * CosteUnitario)
    res = license.price + (unitPricePerUser * extraUsers)

    return res
