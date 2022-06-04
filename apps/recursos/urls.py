from django.urls import path
from .views import *


urlpatterns = [
    path('recursos/', RecursoListAPIView.as_view()),
    path('recursos/<int:id>/', RecursoDetailAPIView.as_view()),
    path('public/', RecursoPublicAPIView.as_view()),
    path('public/<int:id>/', RecursoPublicDetailAPIView.as_view()),
    path('patrocinador/', PatrocinadorListAPIView.as_view()),
    path('patrocinador/<int:id>/', PatrocinadorDetailAPIView.as_view()),
    path('patrocinador/public/', PatrocinadorPublicAPIView.as_view()),
    path('patrocinador/public/<int:id>/', PatrocinadorPublicDetailAPIView.as_view()),
    path('miembro_proyecto/', MiembroProyectoListAPIView.as_view()),
    path('miembro_proyecto/<int:id>/', MiembroProyectoDetailAPIView.as_view()),
    path('miembro_proyecto/public/', MiembroProyectoPublicAPIView.as_view()),
    path('miembro_proyecto/public/<int:id>/', MiembroProyectoPublicDetailAPIView.as_view())
]
