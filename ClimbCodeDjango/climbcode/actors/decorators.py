from django.core.exceptions import PermissionDenied
import datetime
from _datetime import date


def user_is_programmer(function):
    """Decorador que verifica que el usuario es de tipo Programador"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'programmer'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def user_is_student(function):
    """Decorador que verifica que el usuario es de tipo Student"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'student'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def user_is_teacher(function):
    """Decorador que verifica que el usuario es de tipo Profesor"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'teacher'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def user_is_school(function):
    """Decorador que verifica que el usuario es de tipo Escuela/Academia"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'school'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def school_license_active(function):
    """Decorador que verifica que el usuario Escuela/Academia tiene una licencia activa"""

    def wrap(request, *args, **kwargs):
        school = request.user.actor.school

        # Fecha actual
        today = datetime.date.today()
        # Obtiene la licencia de la escuela cuya fecha de finalización supere a la actual (es decir, aquella activa)
        license = school.license_set.filter(endDate__gte = today)

        # Valida que la escuela tenga licencia activa
        if (license.count() > 0):
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def user_is_administrator(function):
    """Decorador que verifica que el usuario es de tipo Administrador (y staff)"""

    def wrap(request, *args, **kwargs):
        if (hasattr(request.user.actor, 'administrator') and (request.user.is_staff)):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def user_is_student(function):
    """Decorador que verifica que el usuario es de tipo Estudiante"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'student'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap