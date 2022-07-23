from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SituacionRespuesta(TextChoices):
    BUENA = 'B', _('Buena')
    PASABLE = 'P', _('Pasable')
    MALA = 'M', _('Mala')


class TipoPregunta(TextChoices):
    OPCION_MULTIPLE = 'O', _('Domiciliado')
    RESPUESTA_SIMPRE = 'R', _('Respuesta Simple')


class SituacionPregunta(TextChoices):
    CORRECTA = 'C', _('Correcta')
    INCORRECTA = 'I', _('Incorrecta')

