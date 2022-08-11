from django.urls import path
from .views import *

urlpatterns = [
    path('niveles/', NivelesView.as_view()),
    # docente
    path('curso/', CursoListView.as_view()),
    path('curso/<int:id>/', CursoView.as_view()),
    path('curso/id/<int:id>/', CursoIdView.as_view()),

    path('curso-inscripcion/<int:id>/', CursoInscripcionDetailView.as_view()),
    # estudiante
    path('curso-inscripcion/', CursoInscripcionView.as_view())
]
