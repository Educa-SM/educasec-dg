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
    PENDIENTE = 'A', _('Inscrito') # INICIO cuando se registra con codigo
    RETIRADO = 'R', _('Retirado')
    REPROBADO = 'E', _('Reprobado')
    APROBADO = 'P', _('Aprobado')
    INSCRITO = 'D', _('Inscrito')   # cuando el docente lo aprueba o el docente lo registra