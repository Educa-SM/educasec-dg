
from django.urls import path
from .views import *
urlpatterns = [
    path('docente/', RegisterDocenteView.as_view()),
    path('alumno/', RegisterAlumnoView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
