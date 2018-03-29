from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from actors.forms import EditTeacherForm, RegisterTeacherForm, EditStudentForm, RegisterStudentForm, EditProgrammerProfile, EditProgrammerPass
from actors.models import Teacher, School, Student
from subjects.models import Subject
from django.contrib.auth.decorators import login_required
from actors.decorators import user_is_programmer


def add_subject_aux(request):
    pk1 = request.GET.get('pk1')
    pk2 = request.GET.get('pk2')
    teacher = get_object_or_404(Teacher, pk=pk1)
    subject = Subject.objects.filter(pk=pk2)
    t_subjects = Subject.objects.filter(teacher__userAccount_id=teacher.userAccount_id)

    new_subjects = subject | t_subjects
    teacher.subjects.set(new_subjects)

    teacher.save()

    return HttpResponseRedirect('/actors/teachers/list')

def add_subject_teacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    teachers = Teacher.objects.filter(pk=pk)

    user = request.user

    try:
        school = School.objects.get(userAccount_id=user.id)
        school_subjects_aux = Subject.objects.filter(school_id=school.id)\
        .exclude(teacher__in=teachers)
    except Exception as e:
        school_subjects_aux = Subject.objects.none()

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
    }

    return render(request, 'teachers/add_subjects.html', data)

def list_teachers(request):
    user = request.user
    try:
        school = School.objects.get(userAccount_id=user.id)
        teacher_list_aux = Teacher.objects.filter(school_t=school)
    except Exception as e:
        teacher_list_aux = School.objects.none()

    page = request.GET.get('page', 1)
    paginator = Paginator(teacher_list_aux, 6)

    try:
        teacher_list_aux = paginator.page(page)
    except PageNotAnInteger:
        teacher_list_aux = paginator.page(1)
    except EmptyPage:
        teacher_list_aux = paginator.page(paginator.num_pages)

    data = {
        'teacher_list': teacher_list_aux,
        'title': 'Listado de profesores'
    }
    return render(request, 'teachers/list.html', data)

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return HttpResponseRedirect('/actors/teachers/list')
    return render(request, 'teachers/delete.html', {'teacher':teacher})

def edit_teacher(request, pk):
    assert isinstance(request, HttpRequest)
    teacher = get_object_or_404(Teacher, pk=pk)
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

    if (request.method == 'POST'):
        form = RegisterTeacherForm(request.POST, request.FILES)
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

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_t=school)
            except Exception as e:
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            teacher.save()

            return HttpResponseRedirect('/actors/teachers/list')

    else:
        form = RegisterTeacherForm()

    data = {
        'form': form,
        'title': 'Registrar profesor'
    }

    return render(request, 'teachers/register.html', data)

def list_students(request):
    user = request.user
    try:
        school = School.objects.get(userAccount_id=user.id)
        student_list_aux = Student.objects.filter(school_s=school)
    except Exception as e:
        student_list_aux = School.objects.none()

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

    if (request.method == 'POST'):
        form = RegisterStudentForm(request.POST, request.FILES)
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

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_s=school)
            except Exception as e:
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            student.save()

            return HttpResponseRedirect('/actors/students/list')

    else:
        form = RegisterStudentForm()

    data = {
        'form': form,
        'title': 'Registrar estudiante'
    }

    return render(request, 'students/register.html', data)

def edit_student(request, pk):
    assert isinstance(request, HttpRequest)
    student = get_object_or_404(Student, pk=pk)
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
    if request.method == 'POST':
        student.delete()
        return HttpResponseRedirect('/actors/students/list')
    return render(request, 'students/delete.html', {'student':student})


@login_required(login_url='/login/')
@user_is_programmer
def edit_profile_programmer(request):
    """
    Edición del perfil Programador
    """

    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    programmer = request.user.actor.programmer

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditProgrammerProfile(request.POST)
        if (form.is_valid()):
            # Actualiza el User (model Django) en BD
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]            

            userAccount = request.user
            userAccount.email = email
            userAccount.first_name = first_name
            userAccount.last_name = last_name
            userAccount.save()

            # Actualiza el Programador en BD
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]

            programmer.phone = phone
            programmer.photo = photo 
            programmer.dni = dni
            programmer.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        dataForm = {'first_name': programmer.userAccount.first_name, 'last_name': programmer.userAccount.last_name, 'email': programmer.userAccount.email, 
                 'phone': programmer.phone, 'dni': programmer.dni, 'photo': programmer.photo}
        form = EditProgrammerProfile(dataForm)
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'programmer': programmer,
        'titulo': 'Editar Perfil'
    }
        
    return render(request, 'programmers/editProgrammerProfile.html', data)


@login_required(login_url='/login/')
@user_is_programmer
def edit_pass_programmer(request):
    """Edición de la clave del usuario """
    assert isinstance(request, HttpRequest)
    
    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditProgrammerPass(request.POST)
        if (form.is_valid()):
            # Se asegura que la Id que viene del formulario es la misma que la del usuario que realiza la acción
            userAccountId = form.cleaned_data["userAccountId"]
            userAccount = request.user
            if (userAccountId != userAccount.id):
                    return HttpResponseForbidden()

            # Establece la nueva contraseña del usuario
            password = form.cleaned_data["password"]
            userAccount.set_password(password)
            userAccount.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        form = EditProgrammerPass()
    
    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }
        
    return render(request, 'programmers/editProgrammerPass.html', data)



