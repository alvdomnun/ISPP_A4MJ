from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.

#Listado de todos los ejercicios como programador
from actors.decorators import user_is_teacher, user_is_school, user_is_programmer
from actors.models import School
from exercises.models import Exercise


@login_required(login_url='/login/')
@user_is_programmer
def list_exercisesP(request):
    #Filtro por NO draft y Orden de fecha de promocion
    exercise_list = list( Exercise.objects.filter(draft=False).order_by('startPromotionDate'))

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/exercises_programmer.html', data)

#Listado de ejercicios propios como programador
@login_required(login_url='/login/')
@user_is_programmer
def list_own_exercisesP(request):
    programmer = request.user

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
        'title': 'Listado de tus ejercicios'
    }
    return render(request, 'exercises/own_exercises_programmer.html', data)

#Listado de todos los ejercicios como escuela
@login_required(login_url='/login/')
@user_is_school
def list_exercisesS(request):

    # Filtro por NO draft y Orden de fecha de promocion
    exercise_list = list(Exercise.objects.filter(draft=False).order_by('startPromotionDate'))

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/exercises_school.html', data)

#Listado de ejercicios propios como escuela
@login_required(login_url='/login/')
@user_is_school
def list_own_exercisesS(request):
    school = request.user

    #Filtro ejercicios propios
    exercise_list =  Exercise.objects.filter(school__userAccount=school)

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/own_exercises_school.html', data)


#Listado de todos los ejercicios como teacher
@login_required(login_url='/login/')
@user_is_teacher
def list_exercisesT(request):
    #Filtro por NO draft y Orden de fecha de promocion
    exercise_list = list( Exercise.objects.filter(draft=False).order_by('startPromotionDate'))

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/exercises_teacher.html', data)

#Listado de todos los ejercicios de la escuela como teacher
@login_required(login_url='/login/')
@user_is_teacher
def list_school_exercisesT(request):
    teacher = request.user
    # Escuela del teacher
    school = School.objects.get(teacher__userAccount=teacher)
    # Filtro ejercicios propios
    exercise_list = Exercise.objects.filter(school__userAccount=school)

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/exercises_teacher.html', data)


#Listado de todos los ejercicios que enseña el teacher
@login_required(login_url='/login/')
@user_is_teacher
def list_own_exercisesT(request):
    teacher = request.user
    # Escuela del teacher
    school = School.objects.get(teacher__userAccount=teacher)
    # Filtro ejercicios propios
    exercise_list = Exercise.objects.filter(school__userAccount=school).filter(subject__teacher__userAccount=teacher)

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
        'title': 'Listado de ejercicios'
    }
    return render(request, 'exercises/own_exercises_teacher.html', data)