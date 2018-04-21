from django.urls import path

from actors import views

urlpatterns = [
    path('teachers/list', views.list_teachers, name='list_teachers'),
    path('teachers/edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('teachers/register', views.register_teacher, name='register_teacher'),
    path('teachers/edit/delete/<int:pk>', views.delete_teacher, name='delete_teacher'),
    path('teacher/edit', views.edit_self_teacher, name='edit_self_teacher'),
    path('teacher/edit/password', views.edit_self_teacher_pass, name='edit_self_teacher_pass'),

    path('students/list', views.list_students, name='list_students'),
    path('student/register', views.register_student, name='register_student'),
    path('students/edit/<int:pk>', views.edit_student, name='edit_student'),
    path('students/edit/delete/<int:pk>', views.delete_student, name='delete_student'),
    path('students/edit/profile', views.edit_profile_student, name='edit_profile_student'),
    path('students/edit/pass', views.edit_pass_student, name='edit_pass_student'),

    path('programmers/edit/profile', views.edit_profile_programmer, name='edit_profile_programmer'),
    path('programmers/edit/pass', views.edit_pass_programmer, name='edit_pass_programmer'),

    path('schools/edit/profile', views.edit_profile_school, name='edit_profile_school'),
    path('schools/edit/pass', views.edit_pass_school, name='edit_pass_school'),
    path('schools/license/display', views.detail_active_license, name='display_license'),
    path('schools/license/renovation', views.license_renovation, name='license_renovation'),
    path('schools/license/renovation/paypal', views.license_renovation_paypal, name='license_renovation_paypal'),
    path('schools/autorization/display', views.autorization_display, name='autorization_display'),
]
