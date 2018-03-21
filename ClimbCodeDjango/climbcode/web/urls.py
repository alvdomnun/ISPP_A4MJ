from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sampleDashboard', views.sample_dashboard, name="sampleDashboard"),
    path('notebookVistaV1', views.notebookVistaV1, name='notebookVistaV1'),
    path('notebookv1', views.notebookv1, name='notebookv1'),
]