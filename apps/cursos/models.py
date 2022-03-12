from django.db import models
from apps.alumno.models import Alumno
from apps.institucion.models import Docente, Institucion
from educasec.utils.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TipoPregunta(models.TextChoices):
   OPCION_MULTIPLE = 'O', _('Domiciliado')
   RESPUESTA_SIMPRE = 'R', _('Respuesta Simple')

class SituacionPregunta(models.TextChoices):
   CORRECTA = 'C', _('Correcta')
   INCORRECTA = 'I', _('Incorrecta')

# nivel, curso, cuestionario, cuestionario pregunta
# pregunta, alumno curso, pregunta opcion

class Nivel(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)

class Curso(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   nivel_id = models.ForeignKey(Nivel, on_delete=models.CASCADE)
   institucion_id = models.ForeignKey(Institucion, on_delete=models.CASCADE)

class Cuestionario(BaseModel):
   fecha_disponible = models.DateTimeField(auto_now_add=True)
   fecha_expiracion = models.DateTimeField(auto_now_add=True)
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)

   docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)
   curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)


class Pregunta(BaseModel):
   texto = models.CharField('Texto', max_length=150, blank=False, null=False)
   tipo = models.CharField('Tipo de Pregunta', 
            max_length=1,
            choices=TipoPregunta.choices,
            default=TipoPregunta.RESPUESTA_SIMPRE
   )

   docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)
   curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)
   institucion_id = models.ForeignKey(Institucion, on_delete=models.CASCADE)

class CuestionarioPregunta(BaseModel):
   reintentos = models.IntegerField( null=False, default=1)
   puntaje = models.DecimalField( null=False, max_digits=12, decimal_places=2, default=0.0)
   cuestionario_id = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
   pregunta_id = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

class AlumnoCurso(BaseModel):
   periodo = models.IntegerField( null=False, default=1)
   fecha_inscripcion = models.DateTimeField(auto_now_add=True)
   
   alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)
   docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)

class PreguntaOpcion(BaseModel):
   texto = models.CharField(max_length=250, null=False)
   correcta = models.CharField('¿Es correcta?', 
            max_length=1,
            choices=SituacionPregunta.choices,
            default=SituacionPregunta.INCORRECTA
   )
   pregunta_id = models.ForeignKey(Pregunta, on_delete=models.CASCADE)


