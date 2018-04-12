from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
import datetime
from actors.models import School
from licenses.models import License
from subjects.models import Subject
from purchaseTickets.models import PurchaseTicket
from elementPrices.models import ElementPrice
from exercises.forms import BuyExerciseForm
from django.contrib.auth.decorators import login_required
from actors.decorators import user_is_school, user_is_teacher, user_is_programmer
from exercises.models import Exercise
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.http.request import HttpRequest
from _datetime import date



# Create your views here.

@login_required(login_url='/login/')
@user_is_school
def buy_exercise(request, exercise_id):
    """ Compra de un ejercicio """
    assert isinstance(request, HttpRequest)

     # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Obtiene la escuela que va a comprar
    school = request.user.actor.school

    # Obtiene la licencia actual de la escuela que va a comprar
    license = get_license_school(school)
    # Si no se obtiene licencia, es que no tiene licencia activa
    if (not license):
        return HttpResponseForbidden()

    # Obtiene el ejercicio con el ID indicado verificando que no sea un borrador
    exercise = get_object_or_404(Exercise, pk = exercise_id, draft = False)

    # Obtiene la tarifa actual de precios
    elementPrices = ElementPrice.objects.all().first()

    # Detemina si la escuela ha comprado ya el ejercicio o no
    repeatedPurchase = school_repeat_exercise_purchase(exercise, school)

    # Si es una nueva compra y llamada POST
    if (not repeatedPurchase and request.method == 'POST'):
        form = BuyExerciseForm(request.POST)
        if (form.is_valid()):
            # Obtiene los campos del form
            exerciseId = form.cleaned_data["exerciseId"]
            payment = form.cleaned_data["payment"]
            freePurchase = form.cleaned_data["freePurchase"]

            # Si la compra es gratuita
            if (freePurchase == 1):
                # Valida que pueda ser gratis: Licencia asociada a la School con "numFreeExercises" > 0
                if not (license.numFreeExercises > 0):
                     return HttpResponseForbidden()

                # Crea el ticket
                ticket = create_ticket(school, exerciseId, True)

            # Si la compra es via Paypal
            else: 
                # Si el pago se ha ejecutado correctamente, se activa la escuela
                if (payment == 1):
                    # Crea el ticket
                    ticket = create_ticket(school, exerciseId, False)

                # Si el pago no ha sido correcto (payment == 0), recarga la página para que vuelva a intentar el pago
                else:
                    form = BuyExerciseForm()
                    data = {
                        'school': school,
                        'repeatedPurchase': repeatedPurchase,
                        'exercise': exercise,
                        'license': license,
                        'prices': elementPrices,
                        'form': form,
                        'date': date.today(),
                    }

                    return render(request, 'exercisePurchase.html', data)

            # Actualiza la escuela (su licencia) y el ejercicio: comprueba existencia asignaturas y asocia el ejercicio a esta
            update_school_subjects_after_purchase(ticket, license)

            # Actualiza el ejercicio y su programador: +1 en nº ventas (Ejercicio) ; +Precio en el saldo (Programador).
            update_exercise_programmer_after_purchase(ticket, elementPrices)

            return HttpResponseRedirect('/exercises/school/own_list')

        # Si el form no es válido, Forbidden
        else:
            return HttpResponseForbidden()

    else:
        form = BuyExerciseForm()
    
    # Datos del modelo (vista)
    data = {
        'school': school,
        'repeatedPurchase': repeatedPurchase,
        'exercise': exercise,
        'license': license,
        'prices': elementPrices,
        'form': form,
        'date': date.today(),
    }

    return render(request, 'exercisePurchase.html', data)



###################################################     MÉTODOS     PRIVADOS        ##############################################################

def school_repeat_exercise_purchase(exercise, school):
    """ Determina si la escuela ha comprado ya el ejercicio (True) o no (False) """

    # Busca en las compras de la escuela (sus tickets), la compra del ejercicio de Id dado
    repeatedPurchase = school.purchaseticket_set.filter(exercise_id = exercise.id).exists()

    return repeatedPurchase
    

def create_ticket(school, exerciseId, free):
    """ Crea el ticket asociado a la compra """

    price = 0.0
    paymentMethod = 'Free'
    exercise = get_object_or_404(Exercise, pk = exerciseId, draft = False)

    # Si la compra es vía Paypal consulta las tarifas
    if (not free):
        price = ElementPrice.objects.all().first().buyExerciseValue
        paymentMethod = 'Paypal'

    ticket = PurchaseTicket.objects.create(price = price, paymentMethod = paymentMethod, school_id = school.pk, exercise = exercise)

    return ticket


def update_school_subjects_after_purchase(ticket, license):
    """ Actualiza las asignaturas de la escuela a partir del ticket de compra """

    school = ticket.school
    exercise = ticket.exercise

    # Comprueba si la escuela tiene la asignatura del ejercicio
    subjectsQS = Subject.objects.filter(name = exercise.category.name, course = exercise.category.course, school = school)
    # Si no tiene asignatura para ese ejercicio, la crea y asocia el ejercicio
    if (subjectsQS.count() == 0):
        subject = Subject.objects.create(name = exercise.category.name, course = exercise.category.course, school = school)
        subject.exercises.add(exercise)
        subject.save()

    # Si la escuela tiene la asignatura, solo añade el ejercicio
    else:
        subject = subjectsQS[0]
        subject.exercises.add(exercise)
        subject.save()

    # Si el ejercicio se ha comprado de manera gratuita, actualiza la licencia de la escuela (restando una unidad al nº de ejercicios gratis disponibles)
    if (ticket.paymentMethod == 'Free'):
        license.numFreeExercises = license.numFreeExercises - 1
        license.save()


def update_exercise_programmer_after_purchase(ticket, elementPrices):
    """ Actualiza el ejercicio y su programador. """

    # Actualiza el ejercicio: aumento el nº de ventas en 1
    exercise = ticket.exercise
    exercise.sales = exercise.sales + 1
    exercise.save()

    # Obtiene el beneficio real que adquiere el programador por la compra
    price = elementPrices.buyExerciseValue - elementPrices.profitExerciseValue

    # Actualiza el programador: actualiza el saldo 
    programmer = ticket.exercise.programmer
    programmer.balance = programmer.balance + price
    programmer.save()


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

#################################################################################

#Listado de todos los ejercicios como programador
@login_required(login_url='/login/')
def list_exercisesP(request):
    #Filtro por NO draft y Orden de fecha de promocion
    exercise_list = list( Exercise.objects.filter(draft=False).order_by('startPromotionDate'))

    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    #Comprobación de si son ejercicios propios
    ownList = False
    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises_list.html', data)

#Listado de ejercicios propios como programador
@login_required(login_url='/login/')
def list_own_exercisesP(request):

    try:
        programmer = request.user
    except Exception as e:
        return HttpResponseRedirect('/')
    # Comprobación de si son ejercicios propios
    ownList = True
    #Filtro ejercicios propios
    exercise_list =  Exercise.objects.filter(programmer__userAccount=programmer)

    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de tus ejercicios'
    }
    return render(request, 'exercises_list.html', data)


#Listado de todos los ejercicios como escuela
@login_required(login_url='/login/')
def list_exercisesS(request):

    try:
        school = request.user.actor.school
    except Exception as e:
        return HttpResponseRedirect('/')
    # Filtro por NO draft, Orden de fecha de promocion y excluye los que ya tiene comprado
    exercise_list = list(Exercise.objects.filter(draft=False).exclude(school=school).order_by('startPromotionDate'))
    # Comprobación de si son ejercicios propios
    ownList = False
    license = get_license_school(school)
    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'title': 'Listado de ejercicios',
        'ownList': ownList,
        'license':license
    }
    return render(request, 'exercises_list.html', data)

#Listado de ejercicios propios como escuela
@login_required(login_url='/login/')
def list_own_exercisesS(request):
    # Comprobación de si son ejercicios propios
    ownList = True
    try:
        school = request.user.actor.school
    except Exception as e:
        return HttpResponseRedirect('/')
    #Filtro ejercicios propios y NO draft
    exercise_list =  Exercise.objects.filter(school=school).filter(draft=False)

    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises_list.html', data)


#Listado de todos los ejercicios como teacher
@login_required(login_url='/login/')
def list_exercisesT(request):
    #Filtro por NO draft, Orden de fecha de promocion y excluye los que ya tiene comprado la escuela

    try:
        teacher = request.user
    except Exception as e:
        return HttpResponseRedirect('/')
    school = School.objects.get(teacher__userAccount=teacher)
    exercise_list = list( Exercise.objects.filter(draft=False).exclude(school=school).order_by('startPromotionDate'))
    # Comprobación de si son ejercicios propios
    ownList = False
    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises_list.html', data)

#Listado de todos los ejercicios de la escuela como teacher
@login_required(login_url='/login/')
def list_school_exercisesT(request):

    try:
        teacher = request.user
    except Exception as e:
        return HttpResponseRedirect('/')
    # Escuela del teacher
    school = School.objects.get(teacher__userAccount=teacher)
    # Filtro ejercicios propios
    exercise_list = Exercise.objects.filter(school__userAccount=school).filter(draft=False)
    # Comprobación de si son ejercicios propios
    ownList = True

    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises_list.html', data)


#Listado de todos los ejercicios que enseña el teacher
@login_required(login_url='/login/')
def list_own_exercisesT(request):

    try:
        teacher = request.user
    except Exception as e:
        return HttpResponseRedirect('/')
    # Escuela del teacher
    school = School.objects.get(teacher__userAccount=teacher)
    # Filtro ejercicios propios
    exercise_list = Exercise.objects.filter(school__userAccount=school).filter(subject__teacher__userAccount=teacher).filter(draft=False)
    # Comprobación de si son ejercicios propios
    ownList = True
    page = request.GET.get('page', 1)
    paginator = Paginator(exercise_list, 6)

    try:
        exercise_list = paginator.page(page)
    except PageNotAnInteger:
        exercise_list = paginator.page(1)
    except EmptyPage:
        exercise_list = paginator.page(paginator.num_pages)

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises_list.html', data)