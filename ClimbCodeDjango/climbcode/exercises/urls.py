from django.urls import path
from exercises import views

urlpatterns = [
    path(r'buy/<int:exercise_id>', views.buy_exercise, name='buy_exercise'),
]

