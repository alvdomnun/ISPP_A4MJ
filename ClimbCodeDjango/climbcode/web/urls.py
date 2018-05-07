from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    url(r'^pruebaAjaxNotebook$', views.pruebaAjaxNotebook, name='pruebaAjaxNotebook'),
    url(r'^saveNotebook$', views.saveNotebook, name='saveNotebook'),
    url(r'^createNotebook$', views.createNotebook, name='createNotebook'),
    url(r'^editNotebook$', views.editNotebook, name='editNotebook'),
    url(r'^publishNotebook$', views.publishNotebook, name='publishNotebook'),
    url(r'^showNotebook$', views.showNotebook, name='showNotebook'),
    url(r'^previewNotebook$', views.previewNotebook, name='previewNotebook'),

    url(r'^editNotebookAjax$', views.editNotebookAjax, name='editNotebookAjax'),
    url(r'^createUpdateTextBoxAjax$', views.createUpdateTextBoxAjax, name='createUpdateTextBoxAjax'),
    url(r'^deleteTextBoxAjax$', views.deleteTextBoxAjax, name='deleteTextBoxAjax'),
    url(r'^createUpdateCodeBoxAjax$', views.createUpdateCodeBoxAjax, name='createUpdateCodeBoxAjax'),
    url(r'^deleteCodeBoxAjax$', views.deleteCodeBoxAjax, name='deleteCodeBoxAjax'),
    url(r'^createUpdateCodeParamAjax$', views.createUpdateCodeParamAjax, name='createUpdateCodeParamAjax'),
    url(r'^deleteParamAjax$', views.deleteParamAjax, name='deleteParamAjax'),
    url(r'^createUpdateImageBoxAjax$', views.createUpdateImageBoxAjax, name='createUpdateImageBoxAjax'),
    url(r'^deleteImageBoxAjax$', views.deleteImageBoxAjax, name='deleteImageBoxAjax'),
    url(r'^createUpdateCodeIdGraphicAjax$', views.createUpdateCodeIdGraphicAjax, name='createUpdateCodeIdGraphicAjax'),
    url(r'^deleteIdGraphicAjax$', views.deleteIdGraphicAjax, name='deleteIdGraphicAjax'),

    url(r'^iframe_notebook', TemplateView.as_view(template_name="notebook/iframe_notebook.html"),
                   name='iframe_notebook'),

    path('paypal', views.paypalTransaction, name='paypalTransaction'),

    path('balance', views.show_balance, name='show_balance'),
    path('payout', views.createPayout, name='createPayout'),
    path('payout_pay', views.createPayout_pay, name='createPayoutPay'),

]
