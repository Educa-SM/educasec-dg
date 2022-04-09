from django.urls import path
from .views import *

urlpatterns = [
    path('recursos/', RecursoListAPIView.as_view()),
    path('recursos/<int:id>/', RecursoDetailAPIView.as_view()),
]
