from django.urls import path
from .views import *
from .views.preguntas_view import (
    PreguntaCursoView, 
    PreguntaDetailView, 
    PreguntaView,
    PreguntaImagenView
)
from .views.cuestionarios_view import (
    CuestionarioCursoView,
    CuestionarioDetailView,
    CuestionarioView,
    ListCuestionarioAlumnoView,
    ListCuestionarioResueltosView,
    CuestionarioAlumnoView,
    CuestionarioImagenView
)

from .views.solucionarios_view import (
    SolucionCuestionarioView,
    SolucionCursoView
)

urlpatterns = [
    # **** DOCENTE ***************
    path('pregunta_curso/<int:id>/', PreguntaCursoView.as_view()),
    path('pregunta/imagen/<int:id>/', PreguntaImagenView.as_view()),
    path('pregunta/<int:id>/', PreguntaDetailView.as_view()),
    path('pregunta/', PreguntaView.as_view()),
    
    path('cuestionario_curso/<int:id>/', CuestionarioCursoView.as_view()),
    path('cuestionario/imagen/<int:id>/', CuestionarioImagenView.as_view()),
    path('cuestionario/<int:id>/', CuestionarioDetailView.as_view()),
    path('cuestionario/', CuestionarioView.as_view()),

    path('solucion/<int:id>/', SolucionCuestionarioView.as_view()),

    # **** Alumno
    path('alumno/<int:id>/', ListCuestionarioAlumnoView.as_view()),
    path('alumno/<int:id>/resultado/', ListCuestionarioResueltosView.as_view()),
    path('alumno/cuestionario/<int:id>/', CuestionarioAlumnoView.as_view()),
    path('alumno/solucion/', SolucionCursoView.as_view()),
]
