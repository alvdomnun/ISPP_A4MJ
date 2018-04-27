import datetime
import datetime
import logging
import os
import re
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse

from actors.decorators import user_is_programmer, user_is_student, user_is_school, school_license_active, \
    user_is_teacher
from actors.forms import EditProgrammerProfile, EditProgrammerPass, EditStudentPass, EditSchoolProfile, EditSchoolPass, \
    EditStudentProfile, UploadFileForm, EditTeacherProfile, EditTeacherPass
from actors.forms import EditTeacherForm, RegisterTeacherForm, EditStudentForm, RegisterStudentForm
from actors.forms import RenovateLicenseForm
from actors.forms import RenovateLicensePaymentForm
from actors.models import Teacher, School, Student
from climbcode import settings
from licenses.models import License
from licenses.models import LicenseType


@login_required(login_url='/login/')
@user_is_school
@school_license_active
def upload_students(request):

    school = get_object_or_404(School, pk=request.user.id)
    license = get_license_school(school)

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES, user=request.user)

        file_obj = request.FILES.get('file').file

        data = file_obj.read().decode('utf-8')

        rows = re.split('\n', data)

        stop = False
        try:
            for index, row in enumerate(rows):
                if index > 0:
                    if row != "" and row != ";;;;;;":
                        cells = row.split(";")

                        user = User()

                        user.username = cells[0]
                        user.password = cells[1]
                        user.email = cells[2]
                        user.first_name = cells[5]
                        user.last_name = cells[6]

                        student = Student()

                        student.phone = cells[4]
                        student.dni = cells[3]
                        student.userAccount = user
                        student.school_s = school

                        if User.full_clean(user, validate_unique=True) or Student.full_clean(student, exclude=['userAccount']):
                            stop = True
                            break

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
            messages.error(request, 'Compruebe que los datos del fichero cumplan todas las restricciones y pruebe de nuevo, de igual manera recuerde utilizar el mismo archivo de ejemplo')
            return HttpResponseRedirect('/actors/students/upload')

        if form.is_valid() and stop is False:

            try:
                for index, row in enumerate(rows):
                    if index > 0:
                        if row != "" and row != ";;;;;;":
                            try:
                                    cells = row.split(";")

                                    username = cells[0]
                                    password = cells[1]
                                    email = cells[2]

                                    user = User.objects.create_user(username, email, password)

                                    user.first_name = cells[5]
                                    user.last_name = cells[6]

                                    user.save()

                                    student = Student.objects.create(phone=cells[4], dni=cells[3],
                                                                     userAccount=user, school_s=school)

                                    student.save()

                                    license.numUsers = license.numUsers - 1
                                    license.save()

                            except Exception as e:
                                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))

                return HttpResponseRedirect('/actors/students/list')

            except Exception as e:

                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))

    else:
        form = UploadFileForm(user=request.user)

    data = {
        'form': form,
        'title': 'Añadir archivo .csv de estudiantes'
    }

    return render(request, "students/import.html", data)

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def upload_teachers(request):

    school = get_object_or_404(School, pk=request.user.id)
    license = get_license_school(school)


    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES, user=request.user)

        file_obj = request.FILES.get('file').file

        data = file_obj.read().decode('utf-8')

        rows = re.split('\n', data)

        stop = False
        try:
            for index, row in enumerate(rows):
                if index > 0:
                    if row != "" and row != ";;;;;;":
                        cells = row.split(";")

                        user = User()

                        user.username = cells[0]
                        user.password = cells[1]
                        user.email = cells[2]
                        user.first_name = cells[5]
                        user.last_name = cells[6]

                        teacher = Teacher()

                        teacher.phone = cells[4]
                        teacher.dni = cells[3]
                        teacher.userAccount = user
                        teacher.school_t = school

                        if User.full_clean(user, validate_unique=True) or Teacher.full_clean(teacher, exclude=['userAccount']):
                            stop = True
                            break

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
            messages.error(request, 'Compruebe que los datos del fichero cumplan todas las restricciones y pruebe de nuevo, de igual manera recuerde utilizar el mismo archivo de ejemplo')
            return HttpResponseRedirect('/actors/teachers/upload')

        if form.is_valid() and stop is False:

            try:

                print(rows.__len__())

                for index, row in enumerate(rows):
                    if index > 0:
                        if row != "" and row != ";;;;;;":
                            try:
                                    cells = row.split(";")

                                    username = cells[0]
                                    password = cells[1]
                                    email = cells[2]

                                    user = User.objects.create_user(username, email, password)

                                    user.first_name = cells[5]
                                    user.last_name = cells[6]

                                    user.save()

                                    teacher = Teacher.objects.create(phone=cells[4], dni=cells[3],
                                                                     userAccount=user, school_t=school)

                                    teacher.save()

                                    license.numUsers = license.numUsers - 1
                                    license.save()

                            except Exception as e:
                                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))

                return HttpResponseRedirect('/actors/teachers/list')

            except Exception as e:

                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))

    else:
        form = UploadFileForm(user=request.user)

    data = {
        'form': form,
        'title': 'Añadir archivo .csv de profesores'
    }

    return render(request, "teachers/import.html", data)


@login_required(login_url='/login/')
@user_is_teacher
def edit_self_teacher(request):

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    teacher = request.user.actor.teacher

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditTeacherProfile(request.POST)
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

            # Actualiza el Student en BD
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]

            teacher.phone = phone
            teacher.photo = photo
            teacher.dni = dni
            teacher.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        dataForm = {'first_name': teacher.userAccount.first_name, 'last_name': teacher.userAccount.last_name,
                    'email': teacher.userAccount.email,
                    'phone': teacher.phone, 'dni': teacher.dni, 'photo': teacher.photo}
        form = EditTeacherProfile(dataForm)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'teacher': teacher,
        'titulo': 'Editar Perfil'
    }

    return render(request, 'teachers/self_edit.html', data)

@login_required(login_url='/login/')
@user_is_teacher
def edit_self_teacher_pass(request):
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditTeacherPass(request.POST)
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
        form = EditTeacherPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'teachers/self_edit_pass.html', data)

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def list_teachers(request):
    user = request.user

    school = School.objects.get(userAccount_id=user.id)

    try:

        teacher_list_aux = Teacher.objects.filter(school_t=school).order_by()

    except Exception as e:

        teacher_list_aux = Teacher.objects.none()

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

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def delete_teacher(request, pk):

    teacher = get_object_or_404(Teacher, pk=pk)
    school = School.objects.get(userAccount_id=request.user.id)

    if teacher.school_t_id != school.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        user = get_object_or_404(User, pk=teacher.userAccount.id)
        user.delete()
        return HttpResponseRedirect('/actors/teachers/list')

    return render(request, 'teachers/delete.html', {'teacher':teacher})

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def edit_teacher(request, pk):

    teacher = get_object_or_404(Teacher, pk=pk)
    school = School.objects.get(userAccount_id=request.user.id)

    if teacher.school_t_id != school.pk:
        return HttpResponseForbidden()

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
        user = get_object_or_404(User, pk=teacher.userAccount.id)
        user.delete()
    else:
        form = EditTeacherForm()

    data = {
        'form': form,
        'teacher': teacher,
        'title': 'Editar profesor'
    }

    return render(request, 'teachers/edit.html', data)

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

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def register_teacher(request):
    current_school = request.user

    school = School.objects.get(userAccount_id=current_school.id)

    form = RegisterStudentForm(user=request.user)  # Si se pone debajo con el else da error

    if (request.method == 'POST'):
        form = RegisterTeacherForm(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):

            license = get_license_school(school)

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

            # Decremento de 1 en los usuarios de la licencia de la escuela
            license.numUsers = license.numUsers - 1
            license.save()

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_t=school)

            except Exception as e:
                teacher = Teacher.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            teacher.save()

            return HttpResponseRedirect('/actors/teachers/list')

    else:
        form = RegisterTeacherForm(user=current_school)

    data = {
        'form': form,
        'title': 'Registrar profesor',
    }

    return render(request, 'teachers/register.html', data)

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def list_students(request):
    user = request.user

    school = School.objects.get(userAccount_id=user.id)

    try:

        student_list_aux = Student.objects.filter(school_s=school).order_by()

    except Exception as e:

        student_list_aux = Student.objects.none()


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

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def register_student(request):
    current_school = request.user

    school = School.objects.get(userAccount_id=request.user.id)

    form = RegisterStudentForm(user=request.user)# Si se pone debajo con el else da error

    if (request.method == 'POST'):
        form = RegisterStudentForm(request.POST, request.FILES, user=request.user)
        if (form.is_valid()):
            license = get_license_school(school)

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

            # Decremento de 1 en los usuarios de la licencia de la escuela
            license.numUsers = license.numUsers - 1
            license.save()

            userAccount = user

            try:
                school = School.objects.get(userAccount_id=current_school.id)
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount, school_s=school)

            except Exception as e:
                student = Student.objects.create(phone=phone, photo=photo, dni=dni, userAccount=userAccount)

            student.save()

            return HttpResponseRedirect('/actors/students/list')

    data = {
        'form': form,
        'title': 'Registrar estudiante',
    }

    return render(request, 'students/register.html', data)

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def edit_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    school = School.objects.get(userAccount_id=request.user.id)

    if student.school_s_id != school.pk:
        return HttpResponseForbidden()

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
        user = get_object_or_404(User, pk=student.userAccount.id)
        user.delete()
    else:
        form = EditStudentForm()

    data = {
        'form': form,
        'student': student,
        'title': 'Editar estudiante'
    }

    return render(request, 'students/edit.html', data)

@login_required(login_url='/login/')
@user_is_school
@school_license_active
def delete_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    school = School.objects.get(userAccount_id=request.user.id)

    if student.school_s_id != school.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        user = get_object_or_404(User, pk=student.userAccount.id)
        user.delete()
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

@login_required(login_url='/login/')
@user_is_school
def edit_profile_school(request):
    """
    Edición del perfil School
    """

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    school = request.user.actor.school

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditSchoolProfile(request.POST)
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

            # Actualiza el School en BD
            phone = form.cleaned_data["phone"]
            centerName = form.cleaned_data["centerName"]
            identificationCode = form.cleaned_data["identificationCode"]
            postalCode = form.cleaned_data["postalCode"]
            address = form.cleaned_data["address"]

            school.phone = phone
            school.identificationCode = identificationCode
            school.centerName = centerName
            school.postalCode = postalCode
            school.address = address
            school.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        dataForm = {'first_name': school.userAccount.first_name, 'last_name': school.userAccount.last_name,
                    'email': school.userAccount.email,
                    'phone': school.phone, 'identificationCode': school.identificationCode, 'centerName': school.centerName,
                    'postalCode': school.postalCode,'address': school.address,}
        form = EditSchoolProfile(dataForm)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'school': school,
        'titulo': 'Editar Perfil'
    }

    return render(request, 'schools/editSchoolProfile.html', data)

@login_required(login_url='/login/')
@user_is_school
def edit_pass_school(request):
    """Edición de la clave del usuario """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditSchoolPass(request.POST)
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
        form = EditSchoolPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'schools/editSchoolPass.html', data)

@login_required(login_url='/login/')
@user_is_student
def edit_profile_student(request):
    """
    Edición del perfil Student
    """

    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    student = request.user.actor.student

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditStudentProfile(request.POST)
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

            # Actualiza el Student en BD
            phone = form.cleaned_data["phone"]
            photo = form.cleaned_data["photo"]
            dni = form.cleaned_data["dni"]

            student.phone = phone
            student.photo = photo
            student.dni = dni
            student.save()

            return HttpResponseRedirect('/')

    # Si se accede al form vía GET o cualquier otro método
    else:
        dataForm = {'first_name': student.userAccount.first_name, 'last_name': student.userAccount.last_name,
                    'email': student.userAccount.email,
                    'phone': student.phone, 'dni': student.dni, 'photo': student.photo}
        form = EditStudentProfile(dataForm)

    # Datos del modelo (vista)
    data = {
        'form': form,
        'student': student,
        'titulo': 'Editar Perfil'
    }

    return render(request, 'students/editStudentProfile.html', data)

@login_required(login_url='/login/')
@user_is_student
def edit_pass_student(request):
    """Edición de la clave del usuario """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = EditStudentPass(request.POST)
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
        form = EditStudentPass()

    # Datos del modelo (vista)
    data = {
        'form': form,
        'userAccount': request.user,
        'titulo': 'Cambiar credenciales',
    }

    return render(request, 'students/editStudentPass.html', data)

@login_required(login_url='/login/')
@user_is_school
def detail_active_license(request):
    """ Obtiene la licencia activa de la escuela """
    assert isinstance(request, HttpRequest)

    # Valida que el usuario no sea anónimo (esté registrado y logueado)
    if not (request.user.is_authenticated):
        return HttpResponseRedirect('/login/')

    school = request.user.actor.school

    # Obtiene la licencia activa de la escuela
    today = datetime.date.today()
    license = school.license_set.filter(endDate__gte = today)

    # Si hay licencia activa, pantalla de detalle
    if (license.count() > 0):
        license = license.first()
        # Datos del modelo (vista)
        data = {
            'school': school,
            'license': license,
            'date': date.today()
        }

        return render(request, 'schools/licenseDisplay.html', data)

    # Si no hay licensia activa, formulario de renovación
    else:
        form = RenovateLicenseForm()
        license = None
        licenseTypes = LicenseType.objects.all().order_by('price')

        # Datos del modelo (vista)
        data = {
            'form': form,
            'school': school,
            'license': license,
            'licenseTypes': licenseTypes,
            'date': date.today()
        }

        return render(request, 'schools/licenseRenovation.html', data)

@login_required(login_url='/login/')
@user_is_school
def license_renovation(request):
    """
	Renovación de la licencia de una escuela
	"""
    assert isinstance(request, HttpRequest)

    # Si se ha enviado el Form debe ser por POST
    if (request.method == 'POST'):
        form = RenovateLicenseForm(request.POST)
        if (form.is_valid()):
            # Licencia Tipo
            licenseType = form.cleaned_data["licenseType"]
            # Crear la licencia específica en funcion de la licencia tipo (licenseType) y si ha añadido usuarios extras
            licenseType = LicenseType.objects.filter(id = licenseType.id)[0]
            licenseNumUsers = form.cleaned_data["numUsers"]
            licensePrice = getFinalPrice(licenseType, licenseNumUsers)

            # Escuela
            school = request.user.actor.school

            # Crea solo la fecha de inicio, dejando la fecha de fin a None (inactiva)
            today = date.today()
            # Guarda la licencia asociándola a la escuela que renueva
            license = License.objects.create(numUsers = licenseNumUsers, price = licensePrice, numFreeExercises = licenseType.numFreeExercises,
                licenseType = licenseType, school = school)

            paymentData = {
                'school': school,
                'license': license,
                'date': date.today()
            }

            return render(request, 'schools/renovationPayment.html', paymentData)

        # Si la validación falla cargo de nuevo la vista
        else:
            school = request.user.actor.school
            license = None
            licenseTypes = LicenseType.objects.all().order_by('price')

            # Datos del modelo (vista)
            data = {
                'form': form,
                'school': school,
                'license': license,
                'licenseTypes': licenseTypes,
                'date': date.today()
            }

            return render(request, 'schools/licenseRenovation.html', data)
            #return HttpResponseRedirect(reverse('display_license', kwargs={}))

    # Solo se permite acceso vía POST
    else:
        return HttpResponseRedirect(reverse('display_license', kwargs={}))

@login_required(login_url='/login/')
@user_is_school
def license_renovation_paypal(request):
    """
    Controla el pago del usuario
    """
    assert isinstance(request, HttpRequest)

    # Si se ha enviado el Form
    if (request.method == 'POST'):
        form = RenovateLicensePaymentForm(request.POST)
        if (form.is_valid()):
            # Extrae valores y activa el usuario si el pago ha sido correcto
            school = form.cleaned_data["school"]
            license = form.cleaned_data["license"]
            licensePrice = form.cleaned_data["licensePrice"]
            payment = form.cleaned_data["payment"]

            # Obtiene la licencia y la escuela a partir de los Ids que trae el form
            school = School.objects.filter(pk = school).first()
            license = License.objects.filter(id = license).first()

            # Si el pago se ha ejecutado correctamente, se activa la licencia
            if (payment == 1):
                license.endDate = license.startDate + timedelta(days=365)
                license.save()

                return HttpResponseRedirect(reverse('display_license', kwargs={}))

            # Si el pago no ha sido correcto (payment == 0), recarga la página para que vuelva a intentar el pago
            else:
                paymentData = {
                    'school': school,
                    'license': license,
                    'date': date.today()
                }

                return render(request, 'schools/renovationPayment.html', paymentData)
        else:
            # Si el form no es válido, Forbidden
            return HttpResponseForbidden()

    # Si el request no es un POST con el pago, Forbidden
    return HttpResponseForbidden()

@login_required(login_url='/login/')
@user_is_school
def autorization_display(request):
    file_path = os.path.join(settings.STATICFILES_DIRS[0],'Autorization.pdf')
    documentReader = open(file_path, "rb").read()

    return HttpResponse(documentReader, content_type="application/pdf")

@login_required(login_url='/login/')
@user_is_school
def students_upload_example(request):

    import os
    from wsgiref.util import FileWrapper
    from django.conf import settings
    import mimetypes

    file_path = os.path.join(settings.STATICFILES_DIRS[0],'StudentExample.csv')
    download_name = "EjemploEstudiantes.csv"
    wrapper = FileWrapper(open(file_path, "rb"))
    content_type = mimetypes.guess_type(file_path)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name

    return response


@login_required(login_url='/login/')
@user_is_school
def teachers_upload_example(request):

    import os
    from wsgiref.util import FileWrapper
    from django.conf import settings
    import mimetypes

    file_path = os.path.join(settings.STATICFILES_DIRS[0],'TeacherExample.csv')
    download_name = "EjemploProfesores.csv"
    wrapper = FileWrapper(open(file_path, "rb"))
    content_type = mimetypes.guess_type(file_path)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name

    return response

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
