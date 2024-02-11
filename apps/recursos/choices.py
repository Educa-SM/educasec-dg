from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from enum import Enum

class GrupoRecurso(Enum):
    MUNDO_LECTOR = 'M'
    RECURSO = 'R'
    COMPARTIENDO = 'C'

def is_recurso_grupo(grupo):

    return grupo in [
        GrupoRecurso.MUNDO_LECTOR.value, 
        GrupoRecurso.RECURSO.value, 
        GrupoRecurso.COMPARTIENDO.value
    ]

def get_grupo_recurso(grupo) -> list:
    if grupo == GrupoRecurso.MUNDO_LECTOR.value:
        return [
            TipoRecursoChoices.AUDIOLIBRO,
            TipoRecursoChoices.LIBRO_ARCHIVO,
            TipoRecursoChoices.LIBRO_ENLACE

        ]
    if grupo == GrupoRecurso.RECURSO.value:
        return [
            TipoRecursoChoices.FICHA_TRABAJO_ARCHIVO,
            TipoRecursoChoices.FICHA_TRABAJO_ENLACE,
            TipoRecursoChoices.JUEGO_ARCHIVO,
            TipoRecursoChoices.JUEGO_ENLACE,
            TipoRecursoChoices.VIDEO,
        ]
    if grupo == GrupoRecurso.COMPARTIENDO.value:
        return [
            TipoRecursoChoices.PODCAST,
            TipoRecursoChoices.PRODUCCION_AUDIOVISUAL,
            TipoRecursoChoices.PRODUCCION_TEXTOS_ARCHIVO,
            TipoRecursoChoices.PRODUCCION_TEXTOS_ENLACE
        ]
    

class TipoRecursoChoices(TextChoices):
    # MUNDO_LECTOR
    LIBRO_ARCHIVO = 'L', _('Libro (Archivo)')
    LIBRO_ENLACE = 'B', _('Libro (Enlace)')
    AUDIOLIBRO = 'A', _('Audiolibro')

    # RECURSO
    FICHA_TRABAJO_ARCHIVO = 'H', _('Ficha de Trabajo (Archivo)')
    FICHA_TRABAJO_ENLACE = 'F', _('Ficha de Trabajo (Enlace)')
    JUEGO_ARCHIVO = 'G', _('Juego (Archivo)')
    JUEGO_ENLACE = 'J', _('Juego (Enlace)')
    VIDEO = 'Y', _('Video')

    # COMPARTIENDO
    PODCAST = 'P', _('Podcast')
    PRODUCCION_AUDIOVISUAL = 'R', _('Producción Audiovisual')
    PRODUCCION_TEXTOS_ARCHIVO = 'U', _('Producción de Textos (Archivo)')
    PRODUCCION_TEXTOS_ENLACE = 'T', _('Producción de Textos (Enlace)')
   

    def get_value(self):
        return self.value

    def get_label(self):
        return self.label

    def to_dict(self):
        dict = {}
        dict['value'] = self.get_value()
        dict['label'] = self.get_label()
        return dict

class EstadoRecurso(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoTipoJuego(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoJuego(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoOpcionJuego(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoPatrocinador(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoMiembroProyecto(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')