from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TipoDocIdentidad(TextChoices):
    DNI = 'DNI', _('DNI')
    CEX = 'CEX', _('Carnét de Extranjeria')
