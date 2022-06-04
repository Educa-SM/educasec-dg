from django.urls import path
from .views import *


urlpatterns = [
    path('', InstitucionesView.as_view()),
]
