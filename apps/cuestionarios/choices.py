from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EstadoCuestionario(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoPregunta(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoOpcionPregunta(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoSolucion(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoSolucionPregunta(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class SituacionRespuesta(TextChoices):
    BUENA = 'B', _('Buena')
    PASABLE = 'P', _('Pasable')
    MALA = 'M', _('Mala')


class TipoPregunta(TextChoices):
    OPCION_MULTIPLE = 'O', _('Opcion Multiple')
    RESPUESTA_SIMPLE = 'R', _('Respuesta Simple')


class SituacionPregunta(TextChoices):
    CORRECTA = 'C', _('Correcta')
    INCORRECTA = 'I', _('Incorrecta')

