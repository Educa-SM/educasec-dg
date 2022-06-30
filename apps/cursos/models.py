from datetime import datetime as dt
from django.db.models import CharField, DecimalField, ForeignKey, ImageField, IntegerField
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from apps.institucion.models import Alumno, Docente, Institucion
from educasec.utils.defs import upload_to
from educasec.utils.models import BaseModel
from .choices import TipoPregunta, SituacionPregunta


class Nivel(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.nombre


class Grado(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    nivel = ForeignKey(
        Nivel,
        related_name='grados',
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.nombre


class Curso(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    grado = ForeignKey(
        Grado,
        related_name='cursos',
        on_delete=CASCADE,
    )

    def __str__(self):
        return f'{self.nombre} - {self.grado.nombre}'


# *****************   Cuestionario    *******************
class Pregunta(BaseModel):
    texto = CharField(
        'Texto',
        max_length=150,
        blank=False, null=False,
    )
    tipo = CharField(
        'Tipo de Pregunta',
        max_length=1,
        choices=TipoPregunta.choices,
        default=TipoPregunta.RESPUESTA_SIMPRE,
    )
    #imagen = ImageField
    curso = ForeignKey(
        Curso,
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.texto


class PreguntaOpcion(BaseModel):
    texto = CharField(
        max_length=250,
        null=False,
    )
    correcta = CharField(
        '¿Es correcta?',
        max_length=1,
        choices=SituacionPregunta.choices,
        default=SituacionPregunta.INCORRECTA,
    )
    pregunta = ForeignKey(
        Pregunta,
        on_delete=CASCADE,
        related_name='opciones',
    )

    def __str__(self):
        return self.texto


class Cuestionario(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    curso = ForeignKey(
        Curso,
        on_delete=CASCADE,
    )
    imagen = ImageField(
        'Imagen',
        upload_to=upload_to(
            model='cuestionario', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class CuestionarioPregunta(BaseModel):
    intentos_disponibles = IntegerField(
        null=False,
        default=1,
    )
    puntaje_asignado = DecimalField(
        null=False,
        max_digits=12,
        decimal_places=2,
        default=0.0,
    )
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=True,
        null=True,
    )
    cuestionario = ForeignKey(
        Cuestionario,
        on_delete=CASCADE,
        related_name='preguntas',
    )
    pregunta = ForeignKey(
        Pregunta,
        on_delete=CASCADE,
        related_name='cuestionarios_pregunta'
    )

    class Meta:
        unique_together = ('pregunta', 'cuestionario',)

    def __str__(self):
        return self.nombre


# ******************  Inscripcion de Cursos   *********************
class CursoDocente(BaseModel):
    periodo = IntegerField(
        null=False,
        default=1,
    )
    year = IntegerField(
        null=False,
        blank=False,
    )
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    curso = ForeignKey(
        Curso,
        on_delete=CASCADE,
    )
    docente = ForeignKey(
        Docente,
        on_delete=CASCADE,
    )
    institucion = ForeignKey(
        Institucion,
        on_delete=CASCADE,
    )
    codigo_inscripcion = CharField(
        'Codigo',
        max_length=50,
        unique=True,
        null=False,
        blank=True,
    )

    def __str__(self):
        return self.nombre

    def save(self, **kwargs):
        self.codigo_inscripcion = (self.nombre[0] + self.curso.nombre[0] +
                                   self.docente.nombres[0]+self.institucion.nombre[0] +
                                   str(CursoDocente.objects.count()+1))
        super(CursoDocente, self).save(**kwargs)


# la inscripcion -> estado=1(registrado)   estado=2
class AlumnoInscripcionCurso(BaseModel):
    alumno = ForeignKey(
        Alumno,
        on_delete=CASCADE,
    )
    curso_docente = ForeignKey(
        CursoDocente,
        on_delete=CASCADE,
        related_name='inscripciones',
    )

    class Meta:
        unique_together = ('alumno', 'curso_docente',)
