from django.urls import path
from .views import (
    aceptar_docente, RegisterDocenteView, RegisterAlumnoView, 
    LoginView, LogoutView, ChangePasswordView,
    get_estudiante_by_nro_documento, registrar_alumno_curso
)


urlpatterns = [
    path('docente/', RegisterDocenteView.as_view()),
    # aceptar_docente
    path('docente/aceptar/', aceptar_docente, name='aceptar_docente'),
    path('alumno/', RegisterAlumnoView.as_view()),
     path('alumno/curso/', registrar_alumno_curso),
    path('alumno/<str:nro_documento>/', get_estudiante_by_nro_documento),   
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]
