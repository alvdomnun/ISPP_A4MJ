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
from django.urls import path, include
import django.contrib.auth.views
from django.contrib import admin
from datetime import datetime
import web.forms
import web.views
from django.conf.urls import url


admin.autodiscover()

urlpatterns = [
    # Página de bienvenida
    url(r'^$', web.views.index, name='home'),

    # Sesión
    url(r'^login/$', django.contrib.auth.views.login,
        {
            'template_name': 'base/login.html',
            'authentication_form': web.forms.LoginForm,
            'extra_context':
            {
                'titulo': 'Inicio de sesión',
                'year': datetime.now().year,
            },
        },
        name='login'),
    url(r'^logout$', django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^register/programmer$', web.views.register_programmer, name='registerProgrammer'),
    url(r'^register/school$', web.views.register_school, name='registerSchool'),

    # Administrador
    path('admin/', admin.site.urls),

    # Web
    path('web/', include('web.urls')),

    # Profesores
    path('actors/', include('actors.urls')),

    # Asignturas
    path('subjects/', include('subjects.urls')),
]
