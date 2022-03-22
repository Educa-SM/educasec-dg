from django.urls import path
from .views import *

urlpatterns = [
   path('niveles/', NivelesView.as_view()),
   path('curso-docente/', CursoDocenteListView.as_view()),
   path('curso-docente/<int:id>/', CursoDocenteView.as_view()),
   path('curso-inscripcion/', CursoInscripcionView.as_view())
]