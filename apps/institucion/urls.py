from django.urls import path
from .views import *


urlpatterns = [
    path('', InstitucionesView.as_view()),
    path('mensaje-inicio/', MensajeInicioView.as_view()),
    path('mensaje-inicio/<int:id>/', MensajeInicioDetailView.as_view()),
    path('mensajes-hoy/', MensajesHoyView.as_view()),
    path('docentes/pendientes/', get_docentes_pendientes),
    path('docentes/dashboard/', get_info_dashboard_docente)
]
