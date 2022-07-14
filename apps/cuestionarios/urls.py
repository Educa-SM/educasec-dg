from django.urls import path
from .views import *


urlpatterns = [
    path('<int:id>/', CuestionarioCursoView.as_view()),
    path('<int:id>/evaluar/', EvaluarCuestionarioCursoView.as_view()),
    path('alumno/solucion/', SolucionCuestionarioCursoView.as_view()),
    path('solucion/<int:id>/', SolucionCuestionarioView.as_view()),
    path('alumno/<int:id>/', ListCuestionarioAlumnoView.as_view()),
    path('alumno/<int:id>/resultado/', ListCuestionarioResueltosView.as_view()),
    path('alumno/cuestionario/<int:id>/', CuestionarioAlumnoView.as_view()),
]
