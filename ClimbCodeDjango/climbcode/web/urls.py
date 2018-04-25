from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

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
    path('notebookv1_ejercicio_est', views.notebookv1_ejercicio_est, name='notebookv1_ejercicio_est'),
    path('notebookv1aux', views.notebookv1aux, name='notebookv1aux'),
    url(r'^pruebaAjaxNotebook$', views.pruebaAjaxNotebook, name='pruebaAjaxNotebook'),
    url(r'^saveNotebook$', views.saveNotebook, name='saveNotebook'),
    url(r'^createNotebook$', views.createNotebook, name='createNotebook'),
    url(r'^editNotebook$', views.editNotebook, name='editNotebook'),
     url(r'^publishNotebook$', views.publishNotebook, name='publishNotebook'),
    #url(r'^viewNotebook$', views.viewNotebook, name='viewNotebook'),
    url(r'^editNotebookAjax$', views.editNotebookAjax, name='editNotebookAjax'),
    url(r'^createUpdateTextBoxAjax$', views.createUpdateTextBoxAjax, name='createUpdateTextBoxAjax'),
    url(r'^deleteTextBoxAjax$', views.deleteTextBoxAjax, name='deleteTextBoxAjax'),
    url(r'^createUpdateCodeBoxAjax$', views.createUpdateCodeBoxAjax, name='createUpdateCodeBoxAjax'),
    url(r'^deleteCodeBoxAjax$', views.deleteCodeBoxAjax, name='deleteCodeBoxAjax'),
    url(r'^createUpdateCodeParamAjax$', views.createUpdateCodeParamAjax, name='createUpdateCodeParamAjax'),
    url(r'^deleteParamAjax$', views.deleteParamAjax, name='deleteParamAjax'),
    url(r'^createUpdateImageBoxAjax$', views.createUpdateImageBoxAjax, name='createUpdateImageBoxAjax'),
    url(r'^deleteImageBoxAjax$', views.deleteImageBoxAjax, name='deleteImageBoxAjax'),

    url(r'^iframe_notebook', TemplateView.as_view(template_name="notebook/iframe_notebook.html"),
                   name='iframe_notebook'),

    path('paypal', views.paypalTransaction, name='paypalTransaction'),

]
