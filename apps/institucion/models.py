from django.db import models
from apps.seguridad.models import User
from educasec.utils.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TipoDocIdentidad(models.TextChoices):
   DNI = 'DNI', _('DNI')
   CEX = 'CEX', _('Carnét de Extranjeria')

class Institucion(BaseModel):
   nombre = models.CharField('Nombre',max_length=255, null=False, blank=False)
   direccion = models.CharField('Direccion', max_length=255, blank=True, null=True)

class Docente(BaseModel):
   nombres = models.CharField('Nombres',max_length=150, null=False, blank=False)
   apellido_paterno = models.CharField('Apellido Paterno',max_length=150, null=False, blank=False)
   apellido_materno = models.CharField('Apellido Materno',max_length=150, null=False, blank=False)
   direccion = models.CharField('Direccion', max_length=255, blank=True, null=True)
   tipo_documento = models.CharField('Tipo de Documento', 
            max_length=3,
            choices=TipoDocIdentidad.choices,
            default=TipoDocIdentidad.DNI
   )
   nro_documento = models.CharField('Numero de Documento de Identidad',unique=True, max_length=12)
   
   user = models.OneToOneField(User, on_delete=models.CASCADE)

class InstitucionDocente(BaseModel):
   institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
   docente = models.ForeignKey(Docente, on_delete=models.CASCADE)




