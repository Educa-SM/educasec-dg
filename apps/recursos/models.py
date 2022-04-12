from datetime import datetime as dt
from django.db import models
from django.forms import model_to_dict
from apps.institucion.models import Institucion
from apps.recursos.choices import TipoRecursoChoices
from educasec.utils.models import BaseModel
from educasec.utils.defs import upload_to


class Recurso(BaseModel):
    titulo = models.CharField('Título', max_length=500, default='', blank=False, null=False)
    descripcion = models.CharField('Descripción', max_length=500, blank=False, null=False)
    contenido = models.CharField('Contenido', max_length=500, blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=1, choices=TipoRecursoChoices.choices, blank=False, null=False)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    original_filename = models.FileField(
        'Archivo Original',
        upload_to=upload_to(model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True
    )
    miniatura = models.ImageField(
        'Miniatura',
        upload_to=upload_to(model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=False,
        null=False
    )
    def __str__(self):
      return self.titulo

    def to_dict(self):
      dict = model_to_dict(self, exclude=['update_date', 'original_filename', 'miniatura'])
      dict['tipo'] = TipoRecursoChoices(self.tipo).to_dict()
      dict['miniatura'] = self.miniatura.url
      #dict['original_filename'] = self.original_filename.url
      return dict

class TipoJuego(BaseModel):
    nombre = models.CharField('Nombre', max_length=100, null=False, unique=True)
    def __str__(self):
      return self.nombre

class Juego(BaseModel):
    texto = models.CharField('Texto', max_length=255, null=True, blank=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    tipo_juego = models.ForeignKey(TipoJuego, on_delete=models.CASCADE)
    def __str__(self):
      return self.texto

class OpcionJuego(BaseModel):
    pregunta = models.CharField('Pregunta', blank=True, null=True, max_length=255)
    texto = models.CharField('Texto', max_length=255, blank=False, null=False)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    def __str__(self):
      return self.texto
