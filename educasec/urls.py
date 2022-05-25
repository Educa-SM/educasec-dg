from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/cursos/', include('apps.cursos.urls')),
    path('api/recursos/', include('apps.recursos.urls')),
    path('api/cuestionarios/', include('apps.cuestionarios.urls')),
    path('api/institucion/', include('apps.institucion.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
