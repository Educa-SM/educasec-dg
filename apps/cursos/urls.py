from django.urls import path
from .views import *

urlpatterns = [
   path('niveles/', NivelesView.as_view()),
   #docente
   path('curso-docente/', CursoDocenteListView.as_view()),
   path('curso-docente/<int:id>/', CursoDocenteView.as_view()),
   path('curso-docente/id/<int:id>/',CursoDocenteIdView.as_view()),
   path('curso-inscripcion/<int:id>/', CursoInscripcionDocenteView.as_view()),
   path('banco-pregunta/<int:id>/', PreguntasBancoView.as_view()),
   path('banco-cuestionario/<int:id>/', CuestionarioBancoView.as_view()),
   
   #estudiante
   path('curso-inscripcion/', CursoInscripcionView.as_view())
]