from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class GroupChoices(IntegerChoices):
    ADMIN_SISTEMA = 1, _('Administrador del Sistema')
    DOCENTE = 2, _('Docente')
    ADMIN_RECURSOS = 3, _('Administrador de Recursos')
    ALUMNO = 4, _('Alumno')

    def get_value(self):
        return self.value

    def get_label(self):
        return self.label

    def to_dict(self):
        dict = {}
        dict['value'] = self.get_value()
        dict['label'] = self.get_label()
        return dict
