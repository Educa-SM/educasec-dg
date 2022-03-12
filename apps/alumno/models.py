from django.db import models
from apps.cursos.models import Cuestionario, Pregunta, PreguntaOpcion
from apps.institucion.models import Institucion
from educasec.utils.models import BaseModel


class Alumno(BaseModel):
   nombres = models.CharField('Nombres', max_length=150, blank=False)
   apellido_paterno = models.CharField('Apellido Paterno', max_length=150, blank=False)
   apellido_materno = models.CharField('Apellido Materno', max_length=150, blank=False)
   institucion_id = models.ForeignKey(Institucion, on_delete=models.CASCADE)

class SolucionCuestionario(BaseModel):
   fecha_solucion = models.DateTimeField('Fecha de Solucion')
   fecha_revision = models.DateTimeField('Apellido Paterno')
   alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   cuestionario_id = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)


class SolucionPregunta(BaseModel):
   #cuando se responde la pregunta
   respuesta = models.CharField('Respuesta', max_length=250, blank=False)
   puntaje = models.DecimalField('Puntaje Obtenido', max_digits=10, decimal_places=2, blank=False,default=0)
   intentos = models.IntegerField('Intentos',  blank=False, default=0)

   #datos asignados al inicio
   intentos_posibles = models.IntegerField('Cantidad de Intentos',  blank=False, default=0)
   puntaje_pregunta = models.DecimalField('Puntaje de la Pregunta', max_digits=14, decimal_places=2,blank=False,default=0)

   solucion_id = models.ForeignKey(SolucionCuestionario, on_delete=models.CASCADE)
   pregunta_id = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
   opcion_id = models.ForeignKey(PreguntaOpcion, on_delete=models.CASCADE)

   """
   Los intentos_posibles y puntaje_pregunta son asignados por el docente en un inicio
   """