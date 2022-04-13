from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls.conf import re_path
from django.views.static import serve
from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seguridad/', include('apps.seguridad.urls')),
    path('api/cursos/', include('apps.cursos.urls')),
    path('api/recursos/', include('apps.recursos.urls')),
    path('api/cuestionarios/', include('apps.cuestionarios.urls'))

]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root':settings.MEDIA_ROOT
        })
    ]
