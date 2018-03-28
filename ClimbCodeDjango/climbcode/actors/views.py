from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from actors.forms import EditTeacherForm, RegisterTeacherForm, EditStudentForm, RegisterStudentForm
from actors.models import Teacher, School, Student
from subjects.models import Subject


#Para profesores
def remove_subject_aux(request):

    try:
        School.objects.get(userAccount_id=request.user.id)
    except Exception as e:
        return HttpResponseRedirect('/')

    pk1 = request.GET.get('pk1')
    pk2 = request.GET.get('pk2')
    teacher = get_object_or_404(Teacher, pk=pk1)

    try:
        school = School.objects.get(userAccount_id=request.user.id)

        if teacher.school_t_id != school.pk:
            raise Exception("El profesor no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')

    new_subjects = Subject.objects.filter(teacher__userAccount_id=teacher.userAccount_id) \
        .exclude(pk=pk2)

    teacher.subjects.set(new_subjects)

    teacher.save()

    return HttpResponseRedirect('/actors/teachers/list')

#Para estudiantes
def remove_subject_aux2(request):

    try:
        School.objects.get(userAccount_id=request.user.id)
    except Exception as e:
        return HttpResponseRedirect('/')

    pk1 = request.GET.get('pk1')
    pk2 = request.GET.get('pk2')
    student = get_object_or_404(Student, pk=pk1)

    try:
        school = School.objects.get(userAccount_id=request.user.id)

        if student.school_s_id != school.pk:
            raise Exception("El profesor no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')

    new_subjects = Subject.objects.filter(teacher__userAccount_id=student.userAccount_id) \
        .exclude(pk=pk2)

    student.subjects.set(new_subjects)

    student.save()

    return HttpResponseRedirect('/actors/students/list')

#Para profesores
def add_subject_aux(request):

    try:
        School.objects.get(userAccount_id=request.user.id)
    except Exception as e:
        return HttpResponseRedirect('/')

    pk1 = request.GET.get('pk1')
    pk2 = request.GET.get('pk2')
    teacher = get_object_or_404(Teacher, pk=pk1)
    subject = Subject.objects.filter(pk=pk2)

    try:
        school = School.objects.get(userAccount_id=request.user.id)

        if teacher.school_t_id != school.pk:
            raise Exception("El profesor no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')

    t_subjects = Subject.objects.filter(teacher__userAccount_id=teacher.userAccount_id)

    new_subjects = subject | t_subjects
    teacher.subjects.set(new_subjects)

    teacher.save()

    return HttpResponseRedirect('/actors/teachers/list')

#Para estudiantes
def add_subject_aux2(request):

    pk1 = request.GET.get('pk1')
    pk2 = request.GET.get('pk2')

    student = get_object_or_404(Student, pk=pk1)
    subject = Subject.objects.filter(pk=pk2)

    try:
        school = School.objects.get(userAccount_id=request.user.id)

        if student.school_s_id != school.pk:
            raise Exception("El estudiante no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')

    s_subjects = Subject.objects.filter(student__userAccount_id=student.userAccount_id)

    new_subjects = subject | s_subjects
    student.subjects.set(new_subjects)

    student.save()

    return HttpResponseRedirect('/actors/students/list')

def add_subject_teacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    teachers = Teacher.objects.filter(pk=pk)

    user = request.user

    try:
        school = School.objects.get(userAccount_id=user.id)
        subjects_aux = Subject.objects.filter(school_id=school.userAccount_id)
        school_subjects_aux = Subject.objects.filter(school_id=school.userAccount_id) \
            .exclude(teacher__in=teachers)

        if teacher.school_t_id != school.userAccount_id:
            raise Exception("El profesor no pertenece a tu escuela")

    except Exception as e:
        print(e)
        return HttpResponseRedirect('/')


    page = request.GET.get('page', 1)
    paginator = Paginator(school_subjects_aux, 6)

    try:
        school_subjects = paginator.page(page)
    except PageNotAnInteger:
        school_subjects = paginator.page(1)
    except EmptyPage:
        school_subjects = paginator.page(paginator.num_pages)

    data = {
        'school_subjects': school_subjects,
        'teacher': teacher,
        'title': 'Asignar asignaturas',
        'subjects_aux': subjects_aux,
    }

    return render(request, 'teachers/add_subjects.html', data)


def add_subject_student(request, pk):
    student = Student.objects.get(pk=pk)
    students = Student.objects.filter(pk=pk)

    user = request.user

    try:
        school = School.objects.get(userAccount_id=user.id)
        school_subjects_aux = Subject.objects.filter(school=school)\
            .exclude(student__in=students)
        subjects_aux = Subject.objects.filter(school=school)

        if student.school_s_id != school.pk:
            raise Exception("El estudiante no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')


    page = request.GET.get('page', 1)
    paginator = Paginator(school_subjects_aux, 6)

    try:
        school_subjects_aux = paginator.page(page)
    except PageNotAnInteger:
        school_subjects_aux = paginator.page(1)
    except EmptyPage:
        school_subjects_aux = paginator.page(paginator.num_pages)

    data = {
        'school_subjects': school_subjects_aux,
        'student': student,
        'title': 'Asignar asignaturas',
        'subjects_aux': subjects_aux,
    }

    return render(request, 'students/add_subjects.html', data)

def list_teachers(request):
    user = request.user

    try:
        school = School.objects.get(userAccount_id=user.id)
        teacher_list_aux = Teacher.objects.filter(school_t=school)
    except Exception as e:
        return HttpResponseRedirect('/')

    page = request.GET.get('page', 1)
    paginator = Paginator(teacher_list_aux, 6)

    try:
        teacher_list = paginator.page(page)
    except PageNotAnInteger:
        teacher_list = paginator.page(1)
    except EmptyPage:
        teacher_list = paginator.page(paginator.num_pages)

    data = {
        'teacher_list': teacher_list,
        'title': 'Listado de profesores'
    }
    return render(request, 'teachers/list.html', data)

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    try:

        school = School.objects.get(userAccount_id=request.user.id)

        if teacher.school_t_id != school.pk:
            raise Exception("El profesor no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')


    if request.method == 'POST':
        teacher.delete()
        return HttpResponseRedirect('/actors/teachers/list')

    return render(request, 'teachers/delete.html', {'teacher':teacher})

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    try:

        school = School.objects.get(userAccount_id=request.user.id)

        if teacher.school_t_id != school.pk:
            raise Exception("El profesor no pertenece a tu escuela")
    except Exception as e:
        return HttpResponseRedirect('/')

    assert isinstance(request, HttpRequest)
    userAccount = get_object_or_404(User, pk=teacher.userAccount_id)

    if (request.method == 'POST'):
        form = EditTeacherForm(request.POST, request.FILES)
        if (form.is_valid()):
            user = teacher.userAccount

            userAccount.username = user.username
            userAccount.password = user.password
            userAccount.email = form.cleaned_data["email"]
            userAccount.first_name = form.cleaned_data["first_name"]
            userAccount.last_name = form.cleaned_data["last_name"]

            userAccount.save()

            teacher.phone = form.cleaned_data["phone"]
            teacher.photo = form.cleaned_data["photo"]
            teacher.dni = form.cleaned_data["dni"]

            teacher.save()

            return HttpResponseRedirect('/actors/teachers/list')

    elif request.method == 'DELETE':
        teacher.delete()
    else:
        form = EditTeacherForm()

    data = {
        'form': form,
        'teacher': teacher,
        'title': 'Editar profesor'
    }

    return render(request, 'teachers/edit.html', data)

def register_teacher(request):
    current_school = request.user

    try:

        School.objects.get(userAccount_id=current_school.id)

    except Exception as e:
        return HttpResponseRedirect('/')

    form = RegisterStudentForm(user=request.user)  # Si se pone debajo con el else da error
    subjects = form.fields['subjects'].choices

    if (request.method == 'POST'):
        form = RegisterTeacherForm(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Creación del profesor
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]
            subjects = form.cleaned_data["subjects"]

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_t=school)
                # Asignación de las asignaturas
                teacher.subjects.set(subjects)
            except Exception as e:
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            teacher.save()

            return HttpResponseRedirect('/actors/teachers/list')

    else:
        form = RegisterTeacherForm(user=current_school)

    data = {
        'form': form,
        'title': 'Registrar profesor',
        'subjects': subjects,
    }

    return render(request, 'teachers/register.html', data)

def list_students(request):
    user = request.user

    try:
        school = School.objects.get(userAccount_id=user.id)
        student_list_aux = Student.objects.filter(school_s=school)
    except Exception as e:
        return HttpResponseRedirect('/')

    page = request.GET.get('page', 1)
    paginator = Paginator(student_list_aux, 6)

    try:
        student_list_aux = paginator.page(page)
    except PageNotAnInteger:
        student_list_aux = paginator.page(1)
    except EmptyPage:
        student_list_aux = paginator.page(paginator.num_pages)

    data = {
        'student_list': student_list_aux,
        'title': 'Listado de estudiantes'
    }
    return render(request, 'students/list.html', data)

def register_student(request):
    current_school = request.user

    try:

        School.objects.get(userAccount_id=request.user.id)

    except Exception as e:
        return HttpResponseRedirect('/')

    form = RegisterStudentForm(user=request.user)# Si se pone debajo con el else da error
    subjects = form.fields['subjects'].choices

    if (request.method == 'POST'):
        form = RegisterStudentForm(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Creación del estudiante
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]
            subjects = form.cleaned_data["subjects"]

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_s=school)

                # Asignación de las asignaturas
                student.subjects.set(subjects)
            except Exception as e:
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            student.save()

            return HttpResponseRedirect('/actors/students/list')

    data = {
        'form': form,
        'title': 'Registrar estudiante',
        'subjects': subjects,
    }

    return render(request, 'students/register.html', data)

def edit_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    try:

        school = School.objects.get(userAccount_id=request.user.id)

        if student.school_s_id != school.pk:
            raise Exception("El estudiante no pertenece a tu escuela")
    except Exception as e:
        return HttpResponseRedirect('/')

    assert isinstance(request, HttpRequest)
    userAccount = get_object_or_404(User, pk=student.userAccount_id)

    if (request.method == 'POST'):
        form = EditStudentForm(request.POST, request.FILES)
        if (form.is_valid()):
            user = student.userAccount

            userAccount.username = user.username
            userAccount.password = user.password
            userAccount.email = form.cleaned_data["email"]
            userAccount.first_name = form.cleaned_data["first_name"]
            userAccount.last_name = form.cleaned_data["last_name"]

            userAccount.save()

            student.phone = form.cleaned_data["phone"]
            student.photo = form.cleaned_data["photo"]
            student.dni = form.cleaned_data["dni"]

            student.save()

            return HttpResponseRedirect('/actors/students/list')

    elif request.method == 'DELETE':
        student.delete()
    else:
        form = EditStudentForm()

    data = {
        'form': form,
        'student': student,
        'title': 'Editar estudiante'
    }

    return render(request, 'students/edit.html', data)

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    try:

        school = School.objects.get(userAccount_id=request.user.id)

        if student.school_s_id != school.pk:
            raise Exception("El estudiante no pertenece a tu escuela")

    except Exception as e:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        student.delete()
        return HttpResponseRedirect('/actors/students/list')
    return render(request, 'students/delete.html', {'student':student})