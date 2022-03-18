from django.urls import path
from .views import *

urlpatterns = [
   path('niveles/', NivelesView.as_view())
]