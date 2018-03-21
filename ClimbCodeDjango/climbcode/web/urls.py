from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notebookv1', views.notebookv1, name='notebookv1'),
    path('notebookv1aux', views.notebookv1aux, name='notebookv1aux'),
]