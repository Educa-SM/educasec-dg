from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TipoDocIdentidad(TextChoices):
    DNI = 'DNI', _('DNI')
    CEX = 'CEX', _('Carnét de Extranjeria')


class EstadoInstitucion(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

 # estado = A activo, P pendiente, R rechazado
class EstadoDocente(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')
    PENDIENTE = 'P', _('Pendiente')
    RECHAZADO = 'R', _('Rechazado')

class EstadoAlumno(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoMensajeInicio(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')