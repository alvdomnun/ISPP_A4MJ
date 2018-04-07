from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sampleDashboard', views.sample_dashboard, name="sampleDashboard"),
    path('notebookVistaV1', views.notebookVistaV1, name='notebookVistaV1'),
    path('notebookv1', views.notebookv1, name='notebookv1'),
    path('notebookv1_ejercicio_creado', views.notebookv1_ejercicio_creado, name='notebookv1_ejercicio_creado'),
    path('notebookv1_ejercicio_cc', views.notebookv1_ejercicio_cc, name='notebookv1_ejercicio_cc'),
    path('notebookv1_ejercicio_am', views.notebookv1_ejercicio_am, name='notebookv1_ejercicio_am'),
    path('notebookv1_ejercicio_qin', views.notebookv1_ejercicio_qin, name='notebookv1_ejercicio_qin'),
    path('notebookv1aux', views.notebookv1aux, name='notebookv1aux'),

    path('paypal', views.paypalTransaction, name='paypalTransaction'),

]