from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/cursos/', include('apps.cursos.urls')),
    path('api/recursos/', include('apps.recursos.urls')),
    path('api/cuestionarios/', include('apps.cuestionarios.urls'))
]
