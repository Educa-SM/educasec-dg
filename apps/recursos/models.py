from datetime import datetime as dt
from django.db import models
from apps.institucion.models import Institucion
from educasec.utils.models import BaseModel
from educasec.utils.defs import upload_to


class Recurso(BaseModel):
    titulo = models.CharField('Título', max_length=500, default='', blank=False, null=False)
    descripcion = models.CharField('Descripción', max_length=500, blank=False, null=False)
    contenido = models.CharField('Contenido', max_length=500, blank=False, null=False)
    tipo = models.CharField('Tipo', max_length=1, blank=False, null=False)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    original_filename = models.FileField(
        'Archivo Original',
        upload_to=upload_to(model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=False,
        null=False
    )
    miniatura = models.ImageField(
        'Miniatura',
        upload_to=upload_to(model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True
    )

class TipoJuego(BaseModel):
    nombre = models.CharField('Nombre', max_length=100, null=False, unique=True)

class Juego(BaseModel):
    texto = models.CharField('Texto', max_length=255, null=True, blank=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    tipo_juego = models.ForeignKey(TipoJuego, on_delete=models.CASCADE)

class OpcionJuego(BaseModel):
    pregunta = models.CharField('Pregunta', blank=True, null=True, max_length=255)
    texto = models.CharField('Texto', max_length=255, blank=False, null=False)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)