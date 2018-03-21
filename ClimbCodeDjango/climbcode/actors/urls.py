from django.urls import path

from actors import views

urlpatterns = [
    path('teachers/list', views.list_teachers, name='list_teachers'),
    path('teachers/edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('teachers/register', views.register_teacher, name='register_teacher'),
    path('teachers/edit/delete/<int:pk>', views.delete_teacher, name='delete_teacher'),
    path('teachers/add/subjects/<int:pk>', views.add_subject_teacher, name='add_subject_teacher'),
    path(r'teachers/add/subjects/add', views.add_subject_aux, name='add_subject_teacher_aux'),

    path('students/list', views.list_students, name='list_students'),
    path('student/register', views.register_student, name='register_student'),
    path('students/edit/<int:pk>', views.edit_student, name='edit_student'),
    path('students/edit/delete/<int:pk>', views.delete_student, name='delete_student'),
]
