from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from web.forms import RegisterProgrammerForm, RegisterSchoolForm, ExerciseForm
from django.contrib.auth.models import User
from actors.models import School, Programmer
from datetime import datetime
from licenses.models import LicenseType
from provinces.models import Province
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from exercises.models import Exercise
from boxes.models import Box, Text, Code, Picture, Parameter
from defaultSubjects.models import DefaultSubject


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

def createNotebook(request):
    """
    Muestra un formulario para crear un ejercicio y la crea si la petición es POST
    :param request: HttpRequest
    :return: HttpResponse
    """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario sea anónimo (no registrado)
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = ExerciseForm(request.POST)
        if (form.is_valid()):
            # Guarda el User (model Django) en BD
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            level = form.cleaned_data["level"]
            category = form.cleaned_data["category"]

            exercise = Exercise.objects.create(title=title, description=description,sales=0,
                                               promoted=False, draft = True, level=level, category=category)

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
        # TODO MBC COMPROBAR PERMISO EDICION DEL ACTOR LOGADO
        if permisoEditNotebook:
            print("Programmer is allowed to edit this notebook")
            print("Editing notebook with id: "+idNotebook)
            exercise = Exercise.objects.get(id=idNotebook)
            print("El título del notebook recuperado es: "+exercise.title)
            if exercise is not None:
                template = loader.get_template('notebook/edit_notebook_v1.html')
                context = {'exercise':exercise}
                return HttpResponse(template.render(context, request))
        else:
            print("This actor is not allowed to edit this notebook")
        

def permisoEditNotebook(idNotebook):
    tienePermiso = False
    #TODO MBC recuperar actor logado, debe ser programador

    #TODO MBC recuperar notebook

    #TODO MBC comprobar que el notebook tiene como id del programador al logado
    return True


### Llamadas ajax

@csrf_exempt
def editNotebookAjax(request):
    print("Editing notebook by ajax")
    if request.method == 'POST':
        print("metodo post")
        idNotebook = request.POST.get('idNotebook')
        title = request.POST.get('title')
        description = request.POST.get('description')
        #TODO MBC VALIDAR CAMPOS
        print(title) 
        editedExercise = updateNotebook(idNotebook,title,description)
        data = {
            'editedExerciseTitle':editedExercise.title,
            'editedExerciseDescription':editedExercise.description
        }
        return JsonResponse(data)

@csrf_exempt
def createUpdateTextBoxAjax(request):
    print("Creating or updating text box for exercise by Ajax")
    if request.method == 'POST':
        print("post method")
        idNotebook = request.POST.get('idNotebook')
        order = request.POST.get('boxOrder')
        text = request.POST.get('text')
        idBox = request.POST.get('idBox')
        if idBox == 'null':
            idBox = None
        else:
            idBox = int(idBox)
        #TODO MBC VALIDAR CAMPOS, INCLUIDO VALIDAR QUE EL BOX QUE SE ESTÁ EDITANDO (SI YA EXISTE) PERTENECE AL PROGRAMADOR LOGADO
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
        idBox = request.POST.get('idBox')
        if idBox == 'null':
            idBox = None
        else:
            idBox = int(idBox)
        #TODO MBC VALIDAR CAMPOS, INCLUIDO VALIDAR QUE EL BOX QUE SE ESTÁ ELIMINANDO EXISTE Y PERTENECE AL PROGRAMADOR LOGADO
        #Bandera actualización box
        updateBox = False
        if idBox is not None and idBox>0:
           deleteTextBox(idNotebook,idBox)

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
        order = request.POST.get('boxOrder')
        contentCode = request.POST.get('contentCode')
        idBox = request.POST.get('idBox')
        if idBox == 'null':
            idBox = None
        else:
            idBox = int(idBox)
        #TODO MBC VALIDAR CAMPOS, INCLUIDO VALIDAR QUE EL BOX QUE SE ESTÁ EDITANDO (SI YA EXISTE) PERTENECE AL PROGRAMADOR LOGADO

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


# Create code param
@csrf_exempt
def createCodeParamAjax(request):
    print("Creating code param for code box by Ajax")
    if request.method == 'POST':
        print("post method")
        idBox = request.POST.get('idBox')
        paramValue = request.POST.get('paramValue')
        idPkParam = request.POST.get('idPkParam')
        nameIdParam = request.POST.get('nameIdParam')
        print(nameIdParam)
        #TODO MBC VALIDAR CAMPOS
        createdParam = createCodeParam(idBox,paramValue,idPkParam,nameIdParam)
        data = {
            'createdParamId':createdParam.id,
        }
        return JsonResponse(data)

### Servicios CRUD Ejercicios y boxes

# Update notebook
def updateNotebook(idNotebook,title,description):
    #TODO MBC VALIDAR CAMPOS
    exercise = Exercise.objects.get(id=idNotebook)
    exercise.title = title
    exercise.description = description
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

# Create code box
def createCodeParam(idBox,paramValue,idPkParam,nameIdParam):
    #TODO MBC VALIDAR CAMPOS
    codeBox = Code.objects.get(id=idBox)
    param = Parameter.objects.create(code=codeBox,value =paramValue,idName = nameIdParam)
    param.save()
    return param
