from django.contrib import admin
from actors.models import Actor, ActorAdminPanel, Administrator, AdministratorAdminPanel, Programmer, ProgrammerAdminPanel
from actors.models import School, SchoolAdminPanel, Teacher, TeacherAdminPanel, Student, StudentAdminPanel

# Register your models here.
admin.site.register(Actor, ActorAdminPanel)
admin.site.register(Administrator, AdministratorAdminPanel)
admin.site.register(Programmer, ProgrammerAdminPanel)
admin.site.register(School, SchoolAdminPanel)
admin.site.register(Teacher, TeacherAdminPanel)
admin.site.register(Student, StudentAdminPanel)