from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from educasec.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/cursos/', include('apps.cursos.urls')),
    path('api/recursos/', include('apps.recursos.urls')),
    path('api/cuestionarios/', include('apps.cuestionarios.urls')),
    path('api/institucion/', include('apps.institucion.urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
