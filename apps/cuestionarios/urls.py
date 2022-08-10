from django.urls import path
from .views import *


urlpatterns = [
    # **** DOCENTE ***************
    path('banco-pregunta/<int:id>/', PreguntaBancoView.as_view()),
    path('banco-cuestionario/<int:id>/', CuestionarioBancoView.as_view()),
    path('<int:id>/', CuestionarioView.as_view()),

    path('solucion/<int:id>/', SolucionCuestionarioView.as_view()),

    # **** Alumno
    path('alumno/<int:id>/', ListCuestionarioAlumnoView.as_view()),
    path('alumno/<int:id>/resultado/', ListCuestionarioResueltosView.as_view()),
    path('alumno/cuestionario/<int:id>/', CuestionarioAlumnoView.as_view()),
    path('alumno/solucion/', SolucionCursoView.as_view()),
]
