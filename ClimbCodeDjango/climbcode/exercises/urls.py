from django.urls import path
from exercises import views

urlpatterns = [
    path(r'buy/<int:exercise_id>', views.buy_exercise, name='buy_exercise'),

    path('programmer/list', views.list_exercisesP, name='list_exercisesP'),
    path('programmer/own_list', views.list_own_exercisesP, name='list_own_exercisesP'),

    path('school/list', views.list_exercisesS, name='list_exercisesS'),
    path('school/own_list', views.list_own_exercisesS, name='list_own_exercisesS'),

    path('teacher/list', views.list_exercisesT, name='list_exercisesT'),
    path('teacher/school_exercises', views.list_school_exercisesT, name='list_school_exercisesT'),
]

