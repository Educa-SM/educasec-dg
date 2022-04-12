from django.urls import path
from .views import *

urlpatterns = [
    path('recursos/', RecursoListAPIView.as_view()),
    path('recursos/<int:id>/', RecursoDetailAPIView.as_view()),
    path('public/', RecursoPublicView.as_view()),
    path('public/<int:id>', RecursoPublicDetailView.as_view()),
]
