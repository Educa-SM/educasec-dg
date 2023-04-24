from django.urls import path
from .views import *


urlpatterns = [
    # **** DOCENTE ***************
    path('pregunta_curso/<int:id>/', PreguntaCursoView.as_view()),
    path('pregunta/<int:id>/', PreguntaDetailView.as_view()),
    path('pregunta/', PreguntaView.as_view()),
    
    path('cuestionario_curso/<int:id>/', CuestionarioCursoView.as_view()),
    path('cuestionario/<int:id>/', CuestionarioDetailView.as_view()),
    path('cuestionario/', CuestionarioView.as_view()),

    path('solucion/<int:id>/', SolucionCuestionarioView.as_view()),

    # **** Alumno
    path('alumno/<int:id>/', ListCuestionarioAlumnoView.as_view()),
    path('alumno/<int:id>/resultado/', ListCuestionarioResueltosView.as_view()),
    path('alumno/cuestionario/<int:id>/', CuestionarioAlumnoView.as_view()),
    path('alumno/solucion/', SolucionCursoView.as_view()),
]
