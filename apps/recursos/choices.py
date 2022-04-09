from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TipoRecursoChoices(TextChoices):
    AUDIOLIBRO = 'A', _('Audiolibro')
    FICHA_TRABAJO_ARCHIVO = 'H', _('Ficha de Trabajo (Archivo)')
    FICHA_TRABAJO_ENLACE = 'F', _('Ficha de Trabajo (Enlace)')
    JUEGO_ARCHIVO = 'G', _('Juego (Archivo)')
    JUEGO_ENLACE = 'J', _('Juego (Enlace)')
    LIBRO_ARCHIVO = 'L', _('Libro (Archivo)')
    LIBRO_ENLACE = 'B', _('Libro (Enlace)')
    PODCAST = 'P', _('Podcast')
    PRODUCCION_AUDIOVISUAL = 'R', _('Producción Audiovisual')
    PRODUCCION_TEXTOS_ARCHIVO = 'U', _('Producción de Textos (Archivo)')
    PRODUCCION_TEXTOS_ENLACE = 'T', _('Producción de Textos (Enlace)')
    VIDEO = 'Y', _('Video')

    def get_value(self):
        return self.value

    def get_label(self):
        return self.label

    def to_dict(self):
        dict = {}
        dict['value'] = self.get_value()
        dict['label'] = self.get_label()
        return dict
