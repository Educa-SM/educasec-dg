from django.db import models
from apps.cursos.models import Cuestionario, Curso, Pregunta, PreguntaOpcion
from apps.institucion.models import Docente, Institucion, TipoDocIdentidad
from apps.seguridad.models import User
from educasec.utils.models import BaseModel

# Create your models here.


class Alumno(BaseModel):
   nro_documento = models.CharField('Numero de Documento de Identidad',unique=True, max_length=12)
   nombres = models.CharField('Nombres', max_length=150, blank=False)
   apellido_paterno = models.CharField('Apellido Paterno', max_length=150, blank=False)
   apellido_materno = models.CharField('Apellido Materno', max_length=150, blank=False)
   tipo_documento = models.CharField('Tipo de Documento', 
            max_length=3,
            choices=TipoDocIdentidad.choices,
            default=TipoDocIdentidad.DNI
   )

   user = models.OneToOneField(User, on_delete=models.CASCADE)
   institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)

   
class SolucionCuestionario(BaseModel):
   fecha_solucion = models.DateTimeField('Fecha de Solucion')
   fecha_revision = models.DateTimeField('Apellido Paterno')

   alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)


class SolucionPregunta(BaseModel):
   #cuando se responde la pregunta
   respuesta = models.CharField('Respuesta', max_length=250, blank=False)
   puntaje = models.DecimalField('Puntaje Obtenido', max_digits=10, decimal_places=2, blank=False,default=0)
   intentos = models.IntegerField('Intentos',  blank=False, default=0)

   #datos asignados al inicio
   intentos_posibles = models.IntegerField('Cantidad de Intentos',  blank=False, default=0)
   puntaje_pregunta = models.DecimalField('Puntaje de la Pregunta', max_digits=14, decimal_places=2,blank=False,default=0)

   solucion = models.ForeignKey(SolucionCuestionario, on_delete=models.CASCADE)
   pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
   opcion_pregunta = models.ForeignKey(PreguntaOpcion, on_delete=models.CASCADE)

   """
   Los intentos_posibles y puntaje_pregunta son asignados por el docente en un inicio
   """


class AlumnoCurso(BaseModel):
   periodo = models.IntegerField( null=False, default=1)
   fecha_inscripcion = models.DateTimeField(auto_now_add=True)
   
   alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
   docente = models.ForeignKey(Docente, on_delete=models.CASCADE)