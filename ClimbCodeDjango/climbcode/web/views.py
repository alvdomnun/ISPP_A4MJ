import datetime as datetimeSchool
import random
import re
import string
from datetime import datetime, date

import paypalrestsdk
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from paypalrestsdk import Payout

from actors.decorators import user_is_programmer
from actors.models import School, Programmer
from boxes.models import Text, Code, Picture, Parameter
from defaultSubjects.models import DefaultSubject
from exercises.models import Exercise
from licenses.models import LicenseType, License
from provinces.models import Province
from web.forms import RegisterProgrammerForm, RegisterSchoolForm, ExerciseForm
from web.forms import RegisterSchoolPaymentForm


# Create your views here.

def error400(request):
    data = {
        'user': request.user,
    }
    return render(request, '400.html', data)

def error403(request):
    data = {
        'user': request.user,
    }
    return render(request, '403.html', data)

def error404(request):
    data = {
        'user': request.user,
    }
    return render(request, '404.html', data)

def error500(request):
    data = {
        'user': request.user,
    }
    return render(request, '500.html', data)

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

@login_required(login_url='/login/')
@user_is_programmer
def notebookVistaV1(request):
	template = loader.get_template('notebook/notebookVistaV1.html')
	context = {}
	return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1(request):
	template = loader.get_template('web/notebookv1.html')
	context = {}
	return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1aux(request):
	template = loader.get_template('web/notebookv1aux.html')
	context = {}
	return HttpResponse(template.render(context, request))


def notebookv1_ejercicio_creado(request):
    template = loader.get_template('web/notebookv1_ejercicio_creado.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1_ejercicio_cc(request):
    template = loader.get_template('web/notebookv1_ejercicio_cc.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1_ejercicio_am(request):
    template = loader.get_template('web/notebookv1_ejercicio_am.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1_ejercicio_qin(request):
    template = loader.get_template('web/notebookv1_ejercicio_qin.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1_ejercicio_est(request):
    template = loader.get_template('web/notebookv1_ejercicio_est.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def notebookv1_ejercicio_geo(request):
    template = loader.get_template('web/notebookv1_ejercicio_geo.html')
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
        form = RegisterProgrammerForm(request.POST, request.FILES)
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

            user = User.objects.get(username=username)

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return HttpResponseRedirect('/')

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
            if (licenseNumUsers > 0):
                licensePrice = getFinalPrice(licenseType, licenseNumUsers)
            else:
                licensePrice = licenseType.price

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

            # Comprueba si existe ya usuario con estos datos
            existingUser = User.objects.filter(username = username)
            if (existingUser.count() > 0):
                # Si existe es una escuela "bloqueada" -> La elimina
                if not(existingUser[0].is_active) and not(existingUser[0].actor.school.isPayed):
                    existingUser[0].delete()

            # Crea y persiste el User Model (inactivo hasta el pago con Paypal)
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            # Se crean inactivos -> Habrá que activarlo tras el pago de Paypal
            user.is_active = False
            user.save()

            # Asocia el Usuario a la escuela y la persiste
            userAccount = user
            school = School.objects.create(phone = phone, photo = photo, province = province, address = address, type = type, teachingType = teachingType, 
                centerName = centerName, postalCode = postalCode, identificationCode = identificationCode, userAccount = userAccount)

            # Crea las fechas de la licencia
            today = date.today()
            endDate = date(today.year + 1, today.month, today.day)
            # Licencia GRATUITA siempre tiene 0 usuarios
            if (licenseType.price == 0):
                licenseNumUsers = 0
            # Guarda la licencia asociándola a la escuela que se registra
            license = License.objects.create(numUsers = licenseNumUsers, price = licensePrice, numFreeExercises = licenseType.numFreeExercises,
                endDate = endDate, licenseType = licenseType, school = school)

            # Si es la licencia gratuita: activamos usuario y nos saltamos Paypal
            if (licenseType.name == 'GRATUITA'):
                user.is_active = True
                user.save()
                return HttpResponseRedirect('/login/')

            # Si no es licencia grauita: paypal
            paymentData = {
                'school': school,
                'license': license,
                'date': date.today()
            }

            return render(request, 'web/registerPayment.html', paymentData)

        else:
            # Si la validación falla también cargo los datos necesarios
            provinces = Province.objects.all()
            licenses = LicenseType.objects.all().order_by('price')
            types = form.fields['type'].choices
            teachingTypes = form.fields['teachingType'].choices

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = RegisterSchoolForm()

        # Datos del modelo (vista)
        provinces = Province.objects.all()
        licenses = LicenseType.objects.all().order_by('price')
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

@csrf_exempt
def saveNotebook(request):
    print("hemos llegado")
    if request.method == 'POST':
        print("metodo post")
        idValorNotebook = request.POST.get('idValorNotebook')
        print(idValorNotebook)
        province = Province.objects.create(name=idValorNotebook)

        #provinces = Province.objects.all
        template = loader.get_template('web/notebookv1.html')
        context = {
            'province': province,
        }
        return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
@user_is_programmer
def createNotebook(request):
    """
    Muestra un formulario para crear un ejercicio y la crea si la petición es POST
    :param request: HttpRequest
    :return: HttpResponse
    """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo
    if not request.user.is_authenticated:
        template = loader.get_template('notebook/notebook_no_permiso.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    # Comprobar que sea un programador

    user = request.user

    programmer = Programmer.objects.get(actor_ptr_id=request.user.id)

    # Si se ha enviado el Form
    if (programmer is not None and request.method == 'POST'):
        form = ExerciseForm(request.POST)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            level = form.cleaned_data["level"]
            category = form.cleaned_data["category"]

            exercise = Exercise.objects.create(title=title, description=description,sales=0,
                                               promoted=False, draft = True, level=level, category=category, programmer=programmer)

            idNotebook = exercise.id
            return HttpResponseRedirect('/web/editNotebook?idNotebook='+str(idNotebook))

        else:
            # Si la validación falla también cargo los datos necesarios
            categories = DefaultSubject.objects.all()
            levels = form.fields['level'].choices

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = ExerciseForm()

        # Datos del modelo (vista)
        categories = DefaultSubject.objects.all()
        levels = form.fields['level'].choices

    data = {
        'form': form,
        'categories': categories,
        'levels': levels,
    }
    template = loader.get_template('web/createNotebook.html')

    return HttpResponse(template.render(data, request))

def editNotebook(request):
    print("Editing notebook")
    if request.method == 'GET':
        # Petición de edición de notebook existente
        idNotebook = request.GET.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if (permisoEditNotebook(idNotebook,request) and exercise.draft == True):
            print("Programmer is allowed to edit this notebook")
            print("Editing notebook with id: "+idNotebook)
            exercise = Exercise.objects.get(id=idNotebook)
            if exercise is not None:
                template = loader.get_template('notebook/edit_notebook_v1.html')

                boxesText = Text.objects.filter(exercise=exercise)
                boxesView = []
                for box in boxesText:
                    contentEscape = box.content.replace("\n", "\\n")
                    boxTextView = BoxView(box.id,box.exercise.id,box.order,'Text',contentEscape)
                    boxesView.append(boxTextView)

                boxesCode = Code.objects.filter(exercise=exercise)
                for box in boxesCode:
                    contentEscape = box.content.replace("\n", "\\n")
                    paramtersCode = Parameter.objects.filter(code=box)
                    parameters = []
                    for parameter in paramtersCode:
                        parameters.append(parameter)
                    boxCodeView = BoxView(box.id,box.exercise.id,box.order,'Code',box.content.replace("\n", "\\n"),parameters,box.idGraphic)
                    boxesView.append(boxCodeView)

                boxesPicture = Picture.objects.filter(exercise=exercise)
                for box in boxesPicture:
                    boxPictureView = BoxView(box.id,box.exercise.id,box.order,'Picture',box.url)
                    boxesView.append(boxPictureView)

                boxesView.sort(key=lambda x: x.order, reverse=False)
                form = ExerciseForm()

                # Datos del modelo (vista)
                categories = DefaultSubject.objects.all()
                levels = form.fields['level'].choices

                context = {
                    'exercise':exercise,
                    'boxesView':boxesView,
                    'levels':levels,
                    'categories':categories
                }
                return HttpResponse(template.render(context, request))
        else:
            if (not permisoEditNotebook(idNotebook,request)):
                template = loader.get_template('notebook/notebook_no_permiso.html')
                context = {
                }
                return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template('notebook/notebook_publicado.html')
                context = {
                }
                return HttpResponse(template.render(context, request))

def publishNotebook(request):

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo
    if not request.user.is_authenticated:
        template = loader.get_template('notebook/notebook_no_permiso.html')
        context = {
        }
        return HttpResponse(template.render(context, request))

    # Comprobar que sea un programador

    user = request.user

    programmer = Programmer.objects.get(actor_ptr_id=request.user.id)

    # Si se ha enviado el Form
    if (programmer is not None and request.method == 'POST'):
        idExercise = request.POST.get('exerciseId')

        if permisoEditNotebook(idExercise,request):
            publishExercise(idExercise)
            template = loader.get_template('notebook/notebook_publicado_exito.html')
            context = {
            }
            return HttpResponse(template.render(context, request))
            #return HttpResponseRedirect('/exercises/programmer/own_list')
        else:
            template = loader.get_template('notebook/notebook_no_permiso.html')
            context = {
            }
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('notebook/notebook_no_permiso.html')
        context = {
        }
        return HttpResponse(template.render(context, request))
        
def permisoEditNotebook(idNotebook,request):
    tienePermiso = False
    # recuperar actor logado, debe ser programador
    user = request.user
    # recuperar notebook
    exercise = Exercise.objects.get(id=idNotebook)
    # comprobar que el notebook tiene como id del programador al logado
    tienePermiso = exercise.programmer.actor_ptr_id == user.id
    return tienePermiso

def permisoViewRolesEscuelaNotebook(idNotebook,request):
    tienePermiso = False
    # recuperar actor logado, debe ser programador
    user = request.user
    # recuperar notebook
    exercise = Exercise.objects.get(id=idNotebook)
    if hasattr(request.user.actor, 'school'):
        # Comprobar que la escuela ha adquirido el ejercicio
        idSchool = request.user.actor.school.actor_ptr_id
        school = request.user.actor.school
        tienePermiso = isSchoolAdquiredExercise(exercise, school) and schoolActiveLicense(school)
    elif hasattr(request.user.actor, 'student'):
        student = request.user.actor.student
        idSchool = student.school_s_id
        school = School.objects.get(actor_ptr_id=idSchool)
        tienePermiso = isSchoolAdquiredExercise(exercise, school) and schoolActiveLicense(school)
    elif hasattr(request.user.actor, 'teacher'):
        teacher = request.user.actor.teacher
        idSchool = teacher.school_t_id
        school = School.objects.get(actor_ptr_id=idSchool)
        tienePermiso = isSchoolAdquiredExercise(exercise, school) and schoolActiveLicense(school)
    return tienePermiso

def permisoPreviewNotebook(idNotebook,request):
    tienePermiso = False
    # recuperar actor logado, debe ser programador
    user = request.user
    # recuperar notebook
    exercise = Exercise.objects.get(id=idNotebook)
    if hasattr(request.user.actor, 'school') or hasattr(request.user.actor, 'programmer') or hasattr(request.user.actor, 'teacher'):
        if exercise.draft == False:
            tienePermiso = True
    return tienePermiso


def schoolActiveLicense(school):
    # Fecha actual
    today = datetimeSchool.date.today()
    # Obtiene la licencia de la escuela cuya fecha de finalización supere a la actual (es decir, aquella activa)
    license = school.license_set.filter(endDate__gte=today)

    # Valida que la escuela tenga licencia activa
    if (license.count() > 0):
        return True
    else:
        return False

def permisoViewRolProgramadorNotebook(idNotebook,request):
    tienePermiso = False
    # recuperar actor logado, debe ser programador
    user = request.user
    # recuperar notebook
    exercise = Exercise.objects.get(id=idNotebook)
    if hasattr(request.user.actor, 'programmer'):
        programmerId = request.user.actor.programmer.actor_ptr_id
        tienePermiso = exercise.programmer.actor_ptr_id == user.id
    return tienePermiso

def isSchoolAdquiredExercise(exerciseParam,school):
    exerciseAdquired = False
    exercise_list = Exercise.objects.filter(school=school).filter(draft=False)
    for exercise in exercise_list:
        if exercise.id == exerciseParam.id:
            exerciseAdquired = True
            break
    return exerciseAdquired

# Visualización notebook para escuelas, profesores y alumnos
@login_required(login_url='/login/')
def showNotebook(request):
    print("Showing notebook")
    if request.method == 'GET':
        # Petición de edición de notebook existente
        idNotebook = request.GET.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)

        # Si se trata de una escuela, estudiante o profesor, hay que comprobar que la licencia no haya caducado

        if (permisoViewRolesEscuelaNotebook(idNotebook,request) and exercise.draft == False or permisoViewRolProgramadorNotebook(idNotebook,request) or exercise.example == True):
        #if True:
            if exercise is not None:
                template = loader.get_template('notebook/show_notebook.html')
                boxesText = Text.objects.filter(exercise=exercise)
                boxesView = []
                for box in boxesText:
                    contentEscape = box.content.replace("\n", "\\n")
                    boxTextView = BoxView(box.id,box.exercise.id,box.order,'Text',contentEscape)
                    boxesView.append(boxTextView)

                boxesCode = Code.objects.filter(exercise=exercise)
                for box in boxesCode:
                    contentEscape = box.content.replace("\n", "\\n")
                    paramtersCode = Parameter.objects.filter(code=box)
                    parameters = []
                    for parameter in paramtersCode:
                        parameters.append(parameter)
                    boxCodeView = BoxView(box.id,box.exercise.id,box.order,'Code',box.content.replace("\n", "\\n"),parameters,box.idGraphic)
                    boxesView.append(boxCodeView)

                boxesPicture = Picture.objects.filter(exercise=exercise)
                for box in boxesPicture:
                    boxPictureView = BoxView(box.id,box.exercise.id,box.order,'Picture',box.url)
                    boxesView.append(boxPictureView)

                boxesView.sort(key=lambda x: x.order, reverse=False)
                form = ExerciseForm()

                # Datos del modelo (vista)
                categories = DefaultSubject.objects.all()
                levels = form.fields['level'].choices

                context = {
                    'exercise':exercise,
                    'boxesView':boxesView,
                    'levels':levels,
                    'categories':categories
                }
                return HttpResponse(template.render(context, request))
        else:
            errorMessage = 'Permiso denegado'

            if hasattr(request.user.actor, 'school'):
                # Comprobar que la escuela ha adquirido el ejercicio
                idSchool = request.user.actor.school.actor_ptr_id
                school = request.user.actor.school
                if not isSchoolAdquiredExercise(exercise, school):
                    errorMessage = 'La escuela no ha adquirido este ejercicio'
                elif not schoolActiveLicense(school):
                    errorMessage = 'La licencia de la escuela ha caducado'
            elif hasattr(request.user.actor, 'student'):
                student = request.user.actor.student
                idSchool = student.school_s_id
                school = School.objects.get(actor_ptr_id=idSchool)
                if not isSchoolAdquiredExercise(exercise, school):
                    errorMessage = 'La escuela no ha adquirido este ejercicio'
                elif not schoolActiveLicense(school):
                    errorMessage = 'La licencia de la escuela ha caducado'
            elif hasattr(request.user.actor, 'teacher'):
                teacher = request.user.actor.teacher
                idSchool = teacher.school_t_id
                school = School.objects.get(actor_ptr_id=idSchool)
                if not isSchoolAdquiredExercise(exercise, school):
                    errorMessage = 'La escuela no ha adquirido este ejercicio'
                elif not schoolActiveLicense(school):
                    errorMessage = 'La licencia de la escuela ha caducado'

            template = loader.get_template('notebook/notebook_error_message.html')
            context = {
                'errorMessage': errorMessage
            }
            return HttpResponse(template.render(context, request))


# Visualización notebook para escuelas, profesores y alumnos
@login_required(login_url='/login/')
def previewNotebook(request):
    print("Showing notebook")
    if request.method == 'GET':
        # Petición de edición de notebook existente
        idNotebook = request.GET.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)

        # Si se trata de una escuela, estudiante o profesor, hay que comprobar que la licencia no haya caducado

        if (permisoPreviewNotebook(idNotebook,request) and exercise.draft == False):
        #if True:
            if exercise is not None:
                template = loader.get_template('notebook/preview_notebook.html')
                boxesText = Text.objects.filter(exercise=exercise)
                boxesView = []
                for box in boxesText:
                    contentEscape = box.content.replace("\n", "\\n")
                    boxTextView = BoxView(box.id,box.exercise.id,box.order,'Text',contentEscape)
                    boxesView.append(boxTextView)

                boxesCode = Code.objects.filter(exercise=exercise)
                for box in boxesCode:
                    contentEscape = box.content.replace("\n", "\\n")
                    paramtersCode = Parameter.objects.filter(code=box)
                    parameters = []
                    for parameter in paramtersCode:
                        parameters.append(parameter)
                    boxCodeView = BoxView(box.id,box.exercise.id,box.order,'Code',box.content.replace("\n", "\\n"),parameters,box.idGraphic)
                    boxesView.append(boxCodeView)

                boxesPicture = Picture.objects.filter(exercise=exercise)
                for box in boxesPicture:
                    boxPictureView = BoxView(box.id,box.exercise.id,box.order,'Picture',box.url)
                    boxesView.append(boxPictureView)

                boxesView.sort(key=lambda x: x.order, reverse=False)
                form = ExerciseForm()

                # Datos del modelo (vista)
                categories = DefaultSubject.objects.all()
                levels = form.fields['level'].choices

                context = {
                    'exercise':exercise,
                    'boxesView':boxesView,
                    'levels':levels,
                    'categories':categories
                }
                return HttpResponse(template.render(context, request))
        else:
            errorMessage = 'Permiso denegado'

            template = loader.get_template('notebook/notebook_error_message.html')
            context = {
                'errorMessage': errorMessage
            }
            return HttpResponse(template.render(context, request))

### Llamadas ajax

@csrf_exempt
def editNotebookAjax(request):
    print("Editing notebook by ajax")
    if request.method == 'POST':
        print("metodo post")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            title = request.POST.get('title')
            description = request.POST.get('description')
            level = request.POST.get('level')
            category = request.POST.get('category')
            #TODO MBC VALIDAR CAMPOS
            print(title)
            editedExercise = updateNotebook(idNotebook,title,description,level,category)
            data = {
                'editedExerciseTitle':editedExercise.title,
                'editedExerciseDescription':editedExercise.description,
                'editedExerciseLevel': editedExercise.level,
                'editedExerciseCategory': editedExercise.category.name,
                'editedExerciseCategoryId':editedExercise.category.id
            }
            return JsonResponse(data)

@csrf_exempt
def createUpdateTextBoxAjax(request):
    print("Creating or updating text box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            order = request.POST.get('boxOrder')
            text = request.POST.get('text')
            idBox = request.POST.get('idBox')
            if idBox == 'null':
                idBox = None
            else:
                idBox = int(idBox)
            #TODO MBC VALIDAR CAMPOS
            #Bandera actualización box
            updateBox = False
            if idBox is not None and idBox>0:
               savedBox = updateTextBox(idNotebook,order,text,idBox)
               updateBox = True
            else:
               savedBox = createTextBox(idNotebook,order,text)

            data = {
                'savedBoxId':savedBox.id,
                'savedBoxText':savedBox.content,
                'updateBox':updateBox
            }
            return JsonResponse(data)

@csrf_exempt
def deleteTextBoxAjax(request):
    print("Deleting text box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            idBox = request.POST.get('idBox')
            if idBox == 'null':
                idBox = None
            else:
                idBox = int(idBox)
            #TODO MBC VALIDAR CAMPOS
            if idBox is not None and idBox>0:
               deleteTextBox(idNotebook,idBox)

            data = {
            }
            return JsonResponse(data)

# Create code box
@csrf_exempt
def createUpdateImageBoxAjax(request):
    print("Creating or updating image box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            order = request.POST.get('boxOrder')
            url = request.POST.get('url')
            idBox = request.POST.get('idBox')
            if idBox == 'null':
                idBox = None
            else:
                idBox = int(idBox)
            #TODO MBC VALIDAR CAMPOS

            #Bandera actualización box
            updateBox = False
            if idBox is not None and idBox>0:
               savedBox = updateImageBox(idNotebook,order,url,idBox)
               updateBox = True
            else:
               savedBox = createImageBox(idNotebook,order,url)

            data = {
                'savedBoxId':savedBox.id,
                'updateBox':updateBox
            }
            return JsonResponse(data)

# Delete image box
@csrf_exempt
def deleteImageBoxAjax(request):
    print("Deleting image box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            idBox = request.POST.get('idBox')
            if idBox == 'null':
                idBox = None
            else:
                idBox = int(idBox)
            #TODO MBC VALIDAR CAMPOS
            if idBox is not None and idBox>0:
               deleteImageBox(idNotebook,idBox)

            data = {
            }
            return JsonResponse(data)

# Create code box
@csrf_exempt
def createUpdateCodeBoxAjax(request):
    print("Creating or updating code box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            order = request.POST.get('boxOrder')
            contentCode = request.POST.get('contentCode')
            # Validar que el código no contiene funciones no permitidas
            regExp = re.compile('(?:^|\W)(eval\\()|(alert\\()|(window.)|(location.)|(ajax)(?:$|\W)')

            if not regExp.search(contentCode):
                idBox = request.POST.get('idBox')
                if idBox == 'null':
                    idBox = None
                else:
                    idBox = int(idBox)
                #TODO MBC VALIDAR CAMPOS

                #Bandera actualización box
                updateBox = False
                if idBox is not None and idBox>0:
                   savedBox = updateCodeBox(idNotebook,order,contentCode,idBox)
                   updateBox = True
                else:
                   savedBox = createCodeBox(idNotebook,order,contentCode)

                data = {
                    'savedBoxId':savedBox.id,
                    'savedBoxCode':savedBox.content,
                    'updateBox':updateBox
                }

                return JsonResponse(data)

@csrf_exempt
def deleteCodeBoxAjax(request):
    print("Deleting code box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        exercise = Exercise.objects.get(id=idNotebook)
        if permisoEditNotebook(idNotebook, request) and exercise.draft == True:
            idBox = request.POST.get('idBox')
            if idBox == 'null':
                idBox = None
            else:
                idBox = int(idBox)
            #TODO MBC VALIDAR CAMPOS

            if idBox is not None and idBox>0:
               deleteCodeBox(idNotebook,idBox)

            data = {
            }
            return JsonResponse(data)


# Create code param
@csrf_exempt
def createUpdateCodeParamAjax(request):
    print("Creating code param for code box by Ajax")
    if request.method == 'POST':
        print("post method")
        idBox = request.POST.get('idBox')
        paramValue = request.POST.get('paramValue')
        idPkParam = request.POST.get('idPkParam')
        nameIdParam = request.POST.get('nameIdParam')
        nameParam = request.POST.get('nameParam')

        #TODO MBC VALIDAR CAMPOS
        #Bandera actualización param
        updateParam = False

        if idPkParam == 'null':
            idPkParam = None
        else:
            idPkParam = int(idPkParam)

        if idPkParam is not None and idPkParam>0:
           savedParam = updateCodeParam(idBox,paramValue,nameIdParam,idPkParam,nameParam)
           updateParam = True
        else:
           savedParam = createCodeParam(idBox,paramValue,nameIdParam,nameParam)

        data = {
            'savedParamId':savedParam.id,
            'updateParam':updateParam
        }
        return JsonResponse(data)

@csrf_exempt
def deleteParamAjax(request):
    print("Deleting parameter for code box by Ajax")
    if request.method == 'POST':
        print("post method")
        idParam = request.POST.get('idParam')
        if idParam == 'null':
            idParam = None
        else:
            idParam = int(idParam)

        #TODO MBC VALIDAR CAMPOS, INCLUIDO VALIDAR QUE EL BOX QUE SE ESTÁ ELIMINANDO EXISTE Y PERTENECE AL PROGRAMADOR LOGADO
        if idParam is not None and idParam>0:
           deleteParam(idParam)

        data = {
        }
        return JsonResponse(data)

### Servicios CRUD Ejercicios y boxes

# Create image box
def createImageBox(idNotebook,order,url):
    #TODO MBC VALIDAR CAMPOS
    exercise = Exercise.objects.get(id=idNotebook)
    imageBox = Picture.objects.create(exercise=exercise,order=order,url=url)
    imageBox.save()
    return imageBox

# Update image box
def updateImageBox(idNotebook,order,url,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK 
    exercise = Exercise.objects.get(id=idNotebook)
    imageBox = Picture.objects.get(id=idBox)
    imageBox.url = url
    imageBox.save()
    return imageBox

# Delete image box
def deleteImageBox(idNotebook,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK
    exercise = Exercise.objects.get(id=idNotebook)
    imageBox = Picture.objects.get(id=idBox)
    imageBox.delete()

# Update notebook
def updateNotebook(idNotebook,title,description,level,category):
    #TODO MBC VALIDAR CAMPOS
    exercise = Exercise.objects.get(id=idNotebook)
    exercise.title = title
    exercise.description = description
    exercise.level = level
    catego = DefaultSubject.objects.get(id=category)
    exercise.category = catego
    exercise.save()
    return exercise

# Create text box
def createTextBox(idNotebook,order,text):
    #TODO MBC VALIDAR CAMPOS
    exercise = Exercise.objects.get(id=idNotebook)
    textBox = Text.objects.create(exercise=exercise,order=order,content=text)
    textBox.save()
    return textBox

# Update text box
def updateTextBox(idNotebook,order,text,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK 
    exercise = Exercise.objects.get(id=idNotebook)
    textBox = Text.objects.get(id=idBox)
    textBox.content = text
    textBox.save()
    return textBox

# Delete text box
def deleteTextBox(idNotebook,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK
    exercise = Exercise.objects.get(id=idNotebook)
    textBox = Text.objects.get(id=idBox)
    textBox.delete()


# Create code box
def createCodeBox(idNotebook,order,contentCode):
    #TODO MBC VALIDAR CAMPOS
    exercise = Exercise.objects.get(id=idNotebook)
    codeBox = Code.objects.create(exercise=exercise, order=order, content=contentCode)
    codeBox.save()
    return codeBox

# Update code box
def updateCodeBox(idNotebook,order,contentCode,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK 
    exercise = Exercise.objects.get(id=idNotebook)
    codeBox = Code.objects.get(id=idBox)
    codeBox.content = contentCode
    codeBox.save()
    return codeBox

# Delete text box
def deleteCodeBox(idNotebook,idBox):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK
    exercise = Exercise.objects.get(id=idNotebook)
    codeBox = Code.objects.get(id=idBox)
    parameters = Parameter.objects.filter(code=codeBox)
    for parameter in parameters:
        parameter.delete()
    codeBox.delete()

# Create code box
def createCodeParam(idBox,paramValue,nameIdParam,nameParam):
    #TODO MBC VALIDAR CAMPOS
    codeBox = Code.objects.get(id=idBox)
    param = Parameter.objects.create(code=codeBox,value =paramValue,idName = nameIdParam,name=nameParam)
    param.save()
    return param

# Update code box
def updateCodeParam(idBox,paramValue,nameIdParam,idPkParam,nameParam):
    #TODO MBC VALIDAR QUE EL NOTEBOOK PERTENEE AL USUARIO LOGADO
    codeBox = Code.objects.get(id=idBox)
    exercise = Exercise.objects.get(id=codeBox.exercise.id)
    param = Parameter.objects.get(id=idPkParam)
    param.value = paramValue
    param.name = nameParam
    param.save()
    return param

# Delete text box
def deleteParam(idParam):
    ##TODO MBC VALIDAR CAMPOS
    # VALIDAR QUE EL BOX PERTENECE AL NOTEBOOK
    # VALIDAR QUE EL USUARIO LOGADO ES DUEÑO DEL NOTEBOOK
    param = Parameter.objects.get(id=idParam)
    param.delete()

# Publicar ejercicio
def publishExercise(idExercise):
    exercise = Exercise.objects.get(id=idExercise)
    exercise.draft = False
    exercise.save()

class BoxView:
    def __init__(self, id, idExercise, order, type, content, parameters=None, idGraphic=None):
        self.id = id
        self.idExercise = idExercise
        self.order = order
        self.type = type
        self.content = content
        self.parameters = parameters
        self.idGraphic = idGraphic

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

                user = User.objects.get(username=school.userAccount.username)

                user.backend = 'django.contrib.auth.backends.ModelBackend'

                login(request, user)
                return HttpResponseRedirect('/')

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


# Create code param
@csrf_exempt
def createUpdateCodeIdGraphicAjax(request):
    print("Creating code param for code box by Ajax")
    if request.method == 'POST':
        print("post method")
        idBox = request.POST.get('idBox')
        idGraphic = request.POST.get('idGraphic')

        #TODO MBC VALIDAR CAMPOS
        updateCodeIdGrap = updateCodeIdGraphic(idBox,idGraphic)

        data = {
        }
        return JsonResponse(data)

@csrf_exempt
def deleteIdGraphicAjax(request):
    print("Deleting id graphic for code box by Ajax")
    if request.method == 'POST':
        print("post method")
        idBox = request.POST.get('idBox')
        if idBox == 'null':
            idBox = None
        else:
            idBox = int(idBox)

        #TODO MBC VALIDAR CAMPOS, INCLUIDO VALIDAR QUE EL BOX QUE SE ESTÁ ELIMINANDO EXISTE Y PERTENECE AL PROGRAMADOR LOGADO
        if idBox is not None and idBox>0:
           deleteCodeIdGraphic(idBox)

        data = {
        }
        return JsonResponse(data)

# Update id graphic box
def updateCodeIdGraphic(idBox,idGraphic):
    #TODO MBC VALIDAR QUE EL NOTEBOOK PERTENECE AL USUARIO LOGADO
    codeBox = Code.objects.get(id=idBox)
    codeBox.idGraphic = idGraphic
    codeBox.save()
    return codeBox

# Update code box
def deleteCodeIdGraphic(idBox):
    #TODO MBC VALIDAR QUE EL NOTEBOOK PERTENECE AL USUARIO LOGADO
    codeBox = Code.objects.get(id=idBox)
    codeBox.idGraphic = ''
    codeBox.save()
    return codeBox


@login_required(login_url='/login/')
@user_is_programmer
def show_balance(request):
    today = date.today()
    month = today.month + 1
    year = today.year

    today2 = date.today()
    month2 = today2.month + 2
    year2 = today2.year

    if month >= 12:
        month = 1
        year = year + 1

    if month < 10:
        month = str('0' + str(month))
        year = str(year)
    else:
        month = str(month)
        year = str(year)

    if month2 >= 12:
        month2 = 1
        year2 = year2 + 1

    if month2 < 10:
        month2 = str('0' + str(month2))
        year2 = str(year2)
    else:
        month2 = str(month2)
        year2 = str(year2)


    template = loader.get_template('web/saldo.html')

    context = {
        'date': str('25' + "/" + month + "/" + year),
        'date2': str('25' + "/" + month2 + "/" + year2),
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def createPayout(request):

    ## Comprobación para que solo acceda admin o superuser
    if  hasattr(request.user.actor, 'school') or hasattr(request.user.actor, 'programmer') or hasattr(request.user.actor, 'student') or hasattr(request.user.actor, 'teacher'):
        raise PermissionDenied

    #Listado de todos los programadores a pagar
    programmers = Programmer.objects.all().exclude(balance=0.0)

    #Número de programadores a pagar
    num_programmers = programmers.__len__()

    totalBalance = 0
    programmer_list = programmers

    for programmer in programmers:
        try:

            totalBalance += int(programmer.balance)

        except Exception as e:
            programmer_list = Programmer.objects.none()


    #Datos de la vista
    data = {

        'title': 'Saldo',
        'programmer_list':programmer_list,
        'totalBalance':totalBalance,
        'num_programmers':num_programmers

    }
    return render(request, 'web/payout_ex.html', data)

@login_required(login_url='/login/')
def createPayout_pay(request):

    ## Comprobación para que solo acceda admin o superuser
    if  hasattr(request.user.actor, 'school') or hasattr(request.user.actor, 'programmer') or hasattr(request.user.actor, 'student') or hasattr(request.user.actor, 'teacher'):
        raise PermissionDenied

    #Configuración entorno sandbox

    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AYJNcQvaEsYGDlQyjx8fOL43TFMeJd30o0R9bk9vIJOnO8dPiJwxhPGmgrSqQxiQb3v6mjPQKeO-Hzh5",
        "client_secret": "ELgffaZPGDxGRBuMcbOzAPv8ikJG5kUPgWNKgOFnrAZnVlJK-KqGU3Dl1m0Kwj8wB-d_033z7KcBpOk0"
    })

    #Listado de todos los programadores a pagar
    programmers = Programmer.objects.all().exclude(balance=0.0)

    #Número de programadores a pagar
    num_programmers = programmers.__len__()

    totalBalance = 0
    programmer_list = programmers

    #Creamos un Payout por cada programador a pagar
    for programmer in programmers:
        # Configuracion para el envío de Payouts al entorno sandbox, 1 sender por payout
        sender_batch_id = ''.join(
            random.choice(string.ascii_uppercase) for i in range(12))

        #Creación del Payout con su sender, cantidad a pagar del programador (int) y correo del programador a pagar
        payout = Payout({
            "sender_batch_header": {
                "sender_batch_id": sender_batch_id,
                "email_subject": "You have a payment"
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": int(programmer.balance),
                        "currency": "EUR"
                    },
                    "receiver": programmer.userAccount.email,
                    "note": "Thank you.",
                    "sender_item_id": "item_1"
                }
            ]
        })

        try:
            payout.create()
            #Calculamos el balance total que se va a pagar
            totalBalance += int(programmer.balance)

            #Actualizamos el saldo del programador
            programmer.balance = 0.0
            programmer.save()
        except Exception as e:
            programmer_list = Programmer.objects.none()


    #Datos de la vista
    data = {

        'title': 'Saldo',
        'programmer_list':programmer_list,
        'totalBalance':totalBalance,
        'num_programmers':num_programmers

    }
    return render(request, 'web/payout.html', data)
