"""climbcode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from exercises import views


urlpatterns = [
    path('programmer/list', views.list_exercisesP, name='list_exercisesP'),
    path('programmer/own_list', views.list_own_exercisesP, name='list_own_exercisesP'),

    path('school/list', views.list_exercisesS, name='list_exercisesS'),
    path('school/own_list', views.list_own_exercisesS, name='list_own_exercisesS'),

    path('teacher/list', views.list_exercisesT, name='list_exercisesT'),
    path('teacher/list', views.list_school_exercisesT, name='list_school_exercisesT'),
    path('teacher/list', views.list_own_exercisesT, name='list_own_exercisesT'),

]
