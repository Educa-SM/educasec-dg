from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SituacionRespuesta(TextChoices):
    BUENA = 'B', _('Buena')
    PASABLE = 'P', _('Pasable')
    MALA = 'M', _('Mala')
