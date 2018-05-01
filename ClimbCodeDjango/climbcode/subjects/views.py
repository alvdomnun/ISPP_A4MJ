from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from actors.models import Student, School
from exercises.models import Exercise
from subjects.models import Subject

# Create your views here.

#Listado de las asignaturas de cada usuario (school/teacher/student)
@login_required(login_url='/login/')
def list_subjects(request):
    # Comprobación de usuarios
    if hasattr(request.user.actor, 'school'):
        #Recupera la escuela
        school = request.user.actor.school

        # Filtro asignaturas propias de la escuela
        try:
            subject_list = Subject.objects.filter(school=school)
        except Exception as e:
            subject_list = Subject.objects.none()

    elif hasattr(request.user.actor, 'teacher'):
        #Recupera el teacher
        teacher = request.user
        school = School.objects.get(teacher__userAccount=teacher)

        #Filtra las asignaturas por la escuela
        try:
            subject_list = Subject.objects.filter(school=school)
        except Exception as e:
            subject_list = Subject.objects.none()

    elif hasattr(request.user.actor, 'student'):

        # Recupera el student
        student = request.user
        school = School.objects.get(student__userAccount=student)

        # Filtra las asignaturas por la escuela
        try:
            subject_list = Subject.objects.filter(school=school)
        except Exception as e:
            subject_list = Subject.objects.none()

    else:
         raise PermissionDenied


    page = request.GET.get('page', 1)
    paginator = Paginator(subject_list, 6)

    try:
        subject_list = paginator.page(page)
    except PageNotAnInteger:
        subject_list = paginator.page(1)
    except EmptyPage:
        subject_list = paginator.page(paginator.num_pages)

    data = {
        'subject_list': subject_list,
        'title': 'Listado de asignaturas'
    }
    return render(request, 'subjects_list.html', data)

@login_required(login_url='/login/')
def list_subjectsExercises(request,pk):



    if hasattr(request.user.actor, 'school'):

        try:
            # Recupero la asignatura
            subject = Subject.objects.get(pk=pk)

            # Recupera la escuela
            school = request.user.actor.school
            #Ejercicios filtrados por la escuela, NO draft y por la asignatura
            exercise_list = Exercise.objects.filter(school=school).filter(draft=False).filter(subject__exact=subject)
        except Exception as e:
            exercise_list = Exercise.objects.none()

    elif hasattr(request.user.actor, 'teacher'):

        try:
            # Recupero la asignatura
            subject = Subject.objects.get(pk=pk)

            #Recupero al teacher
            teacher = request.user

            #Recupero escuela del teacher
            school = School.objects.get(teacher__userAccount=teacher)

            # Ejercicios filtrados por la escuela del teacher, NO draft y por la asignatura
            exercise_list = Exercise.objects.filter(school=school).filter(draft=False).filter(subject__exact=subject)
        except Exception as e:
            exercise_list = Exercise.objects.none()

    elif hasattr(request.user.actor, 'student'):
        try:
            # Recupero la asignatura
            subject = Subject.objects.get(pk=pk)

            # Recupero al student
            student = request.user

            # Recupero escuela del student
            school = School.objects.get(student__userAccount=student)

            # Ejercicios filtrados por la escuela del student, NO draft y por la asignatura
            exercise_list = Exercise.objects.filter(school=school).filter(draft=False).filter(subject__exact=subject)
        except Exception as e:
            exercise_list = Exercise.objects.none()
    else:
        raise PermissionDenied

    # Lista propia para mostrar el mostrar
    ownList = True

    data = {
        'exercise_list': exercise_list,
        'ownList': ownList,
        'title': 'Listado de ejercicios de asignaturas'
    }
    return render(request, 'exercises_list.html', data)