from django.db import models
from apps.cursos.models import Cuestionario, CursoDocente, PreguntaOpcion
from apps.institucion.models import Alumno

from educasec.utils.models import BaseModel

# Create your models here.

class CuestionarioCurso(BaseModel):
   fecha_asignacion = models.DateTimeField('Fecha de Solucion')
   fecha_expiracion = models.DateTimeField('Apellido Paterno')
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)

   curso_docente = models.ForeignKey(CursoDocente, on_delete=models.CASCADE)
   cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)


class SolucionCuestionario(BaseModel):
   fecha_solucion = models.DateTimeField('Fecha de Solucion')
   fecha_revision = models.DateTimeField('Apellido Paterno')

   alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   cuestionario_curso = models.ForeignKey(CuestionarioCurso, on_delete=models.CASCADE)
   class Meta:
      unique_together = ('alumno', 'cuestionario_curso',)

class SolucionPregunta(BaseModel):
   #cuando se responde la pregunta
   respuesta = models.CharField('Respuesta', max_length=250, blank=False)
   puntaje = models.DecimalField('Puntaje Obtenido', max_digits=10, decimal_places=2, blank=False,default=0)
   intentos = models.IntegerField('Intentos',  blank=False, default=0)

   #datos asignados al inicio
   intentos_posibles = models.IntegerField('Cantidad de Intentos',  blank=False, default=0)
   puntaje_pregunta = models.DecimalField('Puntaje de la Pregunta', max_digits=14, decimal_places=2,blank=False,default=0)

   solucion = models.ForeignKey(SolucionCuestionario, on_delete=models.CASCADE)
   pregunta_opcion = models.ForeignKey(PreguntaOpcion, on_delete=models.CASCADE)

   class Meta:
      unique_together = ('solucion', 'pregunta_opcion',)