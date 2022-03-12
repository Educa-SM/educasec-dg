from django.db import models
from apps.cursos.models import Curso
from educasec.utils.models import BaseModel

# Create your models here.

class Institucion(BaseModel):
   nombre = models.CharField('Nombre',max_length=255, null=False, blank=False)
   direccion = models.CharField('Direccion', max_length=255, blank=True, null=True)

class Docente(BaseModel):
   nombres = models.CharField('Nombres',max_length=150, null=False, blank=False)
   apellido_paterno = models.CharField('Apellido Paterno',max_length=150, null=False, blank=False)
   apellido_materno = models.CharField('Apellido Materno',max_length=150, null=False, blank=False)
   direccion = models.CharField('Direccion', max_length=255, blank=True, null=True)

class InstitucionDocente(BaseModel):
   institucion_id = models.ForeignKey(Institucion, on_delete=models.CASCADE)
   docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)

class DocenteCurso(BaseModel):
   institucion_id = models.ForeignKey(Institucion, on_delete=models.CASCADE)
   docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)
   curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)



