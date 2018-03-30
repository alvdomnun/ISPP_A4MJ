from django.core.exceptions import PermissionDenied


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