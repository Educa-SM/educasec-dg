from django.db import models
from apps.institucion.models import Alumno, Docente, Institucion
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

#*****  Cursos  *
class Nivel(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False, unique=True)
   def __str__(self):
      return self.nombre

class Grado(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   nivel = models.ForeignKey(Nivel,related_name='grados', on_delete=models.CASCADE)
   def __str__(self):
      return self.nombre

class Curso(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   grado = models.ForeignKey(Grado,related_name='cursos', on_delete=models.CASCADE)
   def __str__(self):
      return self.nombre


#*****************   Cuestionario    *******************
class Pregunta(BaseModel):
   texto = models.CharField('Texto', max_length=150, blank=False, null=False)
   tipo = models.CharField('Tipo de Pregunta', 
            max_length=1,
            choices=TipoPregunta.choices,
            default=TipoPregunta.RESPUESTA_SIMPRE
   )
   #imagen = models.ImageField
   curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
   def __str__(self):
      return self.texto

class PreguntaOpcion(BaseModel):
   texto = models.CharField(max_length=250, null=False)
   correcta = models.CharField('¿Es correcta?', 
            max_length=1,
            choices=SituacionPregunta.choices,
            default=SituacionPregunta.INCORRECTA
   )
   pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
   def __str__(self):
      return self.texto

class Cuestionario(BaseModel):
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   #imagen = models.ImageField
   curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
   def __str__(self):
      return self.nombre

class CuestionarioPregunta(BaseModel):
   reintentos = models.IntegerField( null=False, default=1)
   puntaje = models.DecimalField( null=False, max_digits=12, decimal_places=2, default=0.0)
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
   pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
   class Meta:
      unique_together = ('pregunta', 'cuestionario',)
   def __str__(self):
      return self.nombre


# ******************  Inscripcion de Cursos   *********************


class CursoDocente(BaseModel):
   periodo = models.IntegerField( null=False, default=1)
   year = models.IntegerField( null=False, blank=False)
   nombre = models.CharField('Nombre', max_length=150, blank=False, null=False)
   curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
   docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
   institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
   codigo_inscripcion = models.CharField('Codigo',max_length= 50,unique=True,null=False,blank=True)

   def __str__(self) :
      return self.nombre

   def save(self, **kwargs):
      self.codigo_inscripcion = (self.nombre[0] + self.curso.nombre[0]+
                     self.docente.nombres[0]+self.institucion.nombre[0]+
                     str(CursoDocente.objects.count()+1))
      super(CursoDocente, self).save(**kwargs)


# la inscripcion -> estado=1(registrado)   estado=2
class AlumnoInscripcionCurso(BaseModel):
   alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
   curso_docente = models.ForeignKey(CursoDocente, on_delete=models.CASCADE, related_name='inscripciones')
   class Meta:
      unique_together = ('alumno', 'curso_docente',)
