from django.urls import path

from actors import views

urlpatterns = [
    path('teachers/list', views.list_teachers, name='list_teachers'),
    path('teachers/edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('teachers/register', views.register_teacher, name='register_teacher'),
    path('teachers/edit/delete/<int:pk>', views.delete_teacher, name='delete_teacher')
]
