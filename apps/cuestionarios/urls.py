from django.urls import path
from .views import *

urlpatterns = [
   path('<int:id>/', CuestionarioCursoView.as_view()),
   path('alumno/<int:id>/', CuestionarioAlumnoView.as_view())
]