from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EstadoNivel(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoGrado(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')

class EstadoCurso(TextChoices):
    ACTIVO = 'A', _('Activo')
    INACTIVO = 'I', _('Inactivo')
    CERRADO = 'C', _('Cerrado')

class EstadoCursoInscripcion(TextChoices):
    ACTIVO = 'A', _('Inscrito')
    RETIRADO = 'R', _('Retirado')
    APROBADO = 'P', _('Aprobado')
    REPROBADO = 'E', _('Reprobado')