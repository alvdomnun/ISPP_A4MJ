from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from actors.models import Student, School
from exercises.models import Exercise
from subjects.models import Subject

@login_required(login_url='/login/')
def list_subjects_student(request):
    user = request.user

    try:
        student = Student.objects.get(userAccount_id=user.id)
        student_subjects_aux = Subject.objects.filter(student__userAccount_id=student.userAccount.id)
    except Exception as e:
        return HttpResponseRedirect('/')

    page = request.GET.get('page', 1)
    paginator = Paginator(student_subjects_aux, 6)

    try:
        student_subjects = paginator.page(page)
    except PageNotAnInteger:
        student_subjects = paginator.page(1)
    except EmptyPage:
        student_subjects = paginator.page(paginator.num_pages)

    data = {
        'student_subjects': student_subjects,
        'title': 'Asignaturas matriculadas',
    }

    return render(request, 'students/subjects.html', data)

@login_required(login_url='/login/')
def list_subject_exercises(request, pk):
    user = request.user
    subject = Subject.objects.get(pk=pk)
    school = subject.school

    try:
        student = Student.objects.get(userAccount_id=user.id)

        school_aux = student.school_s_id
        if school_aux != school.pk:
            raise Exception('No perteneces a esta escuela')

    except Exception as e:
        print(e)
        return HttpResponseRedirect('/')

    exercises_aux = Exercise.objects.filter(subject=subject)

    page = request.GET.get('page', 1)
    paginator = Paginator(exercises_aux, 6)

    try:
        subject_exercises = paginator.page(page)
    except PageNotAnInteger:
        subject_exercises = paginator.page(1)
    except EmptyPage:
        subject_exercises = paginator.page(paginator.num_pages)

    data = {
        'subject_exercises': subject_exercises,
        'title': 'Ejercicios de la asignatura',
    }

    return render(request, 'students/subject_exercises.html', data)