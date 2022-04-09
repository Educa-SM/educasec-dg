from django.urls import path
from .views import *

urlpatterns = [
   path('<int:id>/', CuestionarioCursoView.as_view())
]