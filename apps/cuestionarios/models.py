from django.db import models
from apps.cursos.models import Cuestionario, CuestionarioPregunta, CursoDocente, PreguntaOpcion
from apps.institucion.models import Alumno
from educasec.utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
# Create your models here.

class SituacionRespuesta(models.TextChoices):
   BUENA = 'B', _('Buena')
   MALA = 'M', _('Mala')
   PASABLE = 'P', _('Pasable')

class CuestionarioCurso(BaseModel):
   fecha_asignacion = models.DateTimeField('Fecha de Solucion')
   fecha_expiracion = models.DateTimeField('Apellido Paterno')
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)

   curso_docente = models.ForeignKey(CursoDocente, on_delete=models.CASCADE)
   cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
   def __str__(self):
      return self.nombre

class SolucionCuestionario(BaseModel):
   fecha_solucion = models.DateTimeField('Fecha de Solucion')
   fecha_revision = models.DateTimeField('Apellido Paterno')
   comentario =  models.CharField('Comentario', max_length=250, blank=True, null=True)

   alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   cuestionario_curso = models.ForeignKey(CuestionarioCurso, on_delete=models.CASCADE)
   class Meta:
      unique_together = ('alumno', 'cuestionario_curso',)
   

class SolucionPregunta(BaseModel):
   #cuando se responde la pregunta
   respuesta = models.CharField('Respuesta', max_length=250, blank=False)
   puntaje_obtenido = models.DecimalField('Puntaje Obtenido', max_digits=10, decimal_places=2, blank=False,default=0)
   intentos_tomados = models.IntegerField('Intentos',  blank=False, default=0)
   comentario =  models.CharField('Comentario', max_length=250, blank=True, null=True)
   situacion_respuesta = models.CharField('Situacion de Respuesta', 
                        max_length=1, 
                        choices=SituacionRespuesta.choices, 
                        default=SituacionRespuesta.PASABLE
   )
   solucion = models.ForeignKey(SolucionCuestionario, on_delete=models.CASCADE)
   cuestionario_pregunta = models.ForeignKey(CuestionarioPregunta, on_delete=models.CASCADE)

   pregunta_opcion = models.ForeignKey(PreguntaOpcion, on_delete=models.SET_NULL, null=True, blank=True)

   class Meta:
      unique_together = ('solucion', 'cuestionario_pregunta',)
   
   def __str__(self):
      return self.respuesta