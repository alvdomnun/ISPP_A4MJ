from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from web.forms import RegisterProgrammerForm, RegisterSchoolForm
from django.contrib.auth.models import User
from actors.models import School, Programmer
from datetime import datetime
from licenses.models import LicenseType
from provinces.models import Province
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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

            # Crea la Escuela y la asocia al User anterior
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            province = form.cleaned_data["province"]
            address = form.cleaned_data["address"]
            postalCode = form.cleaned_data["postalCode"]
            centerName = form.cleaned_data["centerName"]
            type = form.cleaned_data["type"]
            teachingType = form.cleaned_data["teachingType"]
            identificationCode = form.cleaned_data["identificationCode"]
            userAccount = user

            school = School.objects.create(phone = phone, photo = photo, province = province, address = address, type = type, teachingType = teachingType, 
                centerName = centerName, postalCode = postalCode, identificationCode = identificationCode, userAccount = userAccount)

            # TODO: Funcionalidad limitada: no permite añadir extras a la licencia
            licenseType = form.cleaned_data["licenseType"]
            # TODO Crear la licencia en funcion de la licencia tipo (licenseType) y almacenarla para la escuela recién creada (school)

            return HttpResponseRedirect('/login/')

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
        'licenseTitle': 'Licencias Ofertadas',
        'year': datetime.now().year,
    }

    return render(request, 'web/registerSchool.html', data)

@csrf_exempt
def pruebaAjaxNotebook(request):
    print("hemos llegado")
    if request.method == 'POST':
        print("metodo post")
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')

        print(title)
        data = {
            'respuesta': "Recibido en servidor el título: "+title+" y subtítulo: "+subtitle
        }
        return JsonResponse(data)