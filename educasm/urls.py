from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from educasm.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/cursos/', include('apps.cursos.urls')),
    path('api/recursos/', include('apps.recursos.urls')),
    path('api/cuestionarios/', include('apps.cuestionarios.urls')),
    path('api/institucion/', include('apps.institucion.urls')),
    path('docs/', include_docs_urls(title='EDUCASM API')),
    path('', include('apps.inicio.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)