from django.urls import path
from .views import aceptar_docente, RegisterDocenteView, RegisterAlumnoView, LoginView, LogoutView, ChangePasswordView


urlpatterns = [
    path('docente/', RegisterDocenteView.as_view()),
    # aceptar_docente
    path('docente/aceptar/', aceptar_docente, name='aceptar_docente'),
    path('alumno/', RegisterAlumnoView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]
