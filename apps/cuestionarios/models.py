from datetime import datetime as dt
from django.db.models import (
    CharField, ImageField, DateTimeField,
    DecimalField, ForeignKey, IntegerField,
    ManyToManyField
)
from django.db.models.deletion import CASCADE, SET_NULL
from apps.cursos.models import Curso, TipoCurso
from apps.institucion.models import Alumno
from educasec.utils.models import BaseModel
from .choices import SituacionPregunta, SituacionRespuesta, TipoPregunta
from educasec.utils.defs import upload_to


# *****************   Cuestionario    *******************
class PreguntaBanco(BaseModel):
    texto = CharField(
        'Texto',
        max_length=150,
        blank=False, null=False,
    )
    tipo = CharField(
        'Tipo de Pregunta',
        max_length=1,
        choices=TipoPregunta.choices,
        default=TipoPregunta.RESPUESTA_SIMPLE,
    )
    imagen = ImageField(
        'Imagen',
        upload_to=upload_to(model='pregunta_banco', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True,
    )
    tipo_curso = ForeignKey(
        TipoCurso,
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
    pregunta_banco = ForeignKey(
        PreguntaBanco,
        on_delete=CASCADE,
        related_name='opciones',
    )

    def __str__(self):
        return self.texto


class CuestionarioBanco(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
    )
    tipo_curso = ForeignKey(
        TipoCurso,
        on_delete=CASCADE
    )
    imagen = ImageField(
        'Imagen',
        upload_to=upload_to(
            model='cuestionario_banco',
            path=dt.today().strftime('%Y/%m/%d')
        ),
        blank=True,
        null=True,
    )
    preguntas_banco = ManyToManyField(PreguntaBanco)

    def __str__(self):
        return self.nombre


class Cuestionario(BaseModel):
    fecha_asignacion = DateTimeField(
        'Fecha de Asignacion',
    )
    fecha_expiracion = DateTimeField(
        'Fecha de Expiracion',
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
    cuestionario_banco = ForeignKey(
        CuestionarioBanco,
        on_delete=CASCADE,
        related_name='cuestionarios'
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
        related_name='cuestionario_preguntas',
    )
    pregunta_banco = ForeignKey(
        PreguntaBanco,
        on_delete=CASCADE,
        related_name='cuestionario_preguntas'
    )

    class Meta:
        unique_together = ('pregunta_banco', 'cuestionario',)

    def __str__(self):
        return self.nombre


class Solucion(BaseModel):
    fecha_solucion = DateTimeField(
        'Fecha de Solucion',
        auto_now_add=True,
    )
    fecha_revision = DateTimeField(
        'Fecha Revision',
        blank=True,
        null=True,
    )
    comentario = CharField(
        'Comentario',
        max_length=250,
        blank=True,
        null=True,
    )
    alumno = ForeignKey(
        Alumno,
        on_delete=CASCADE,
    )
    cuestionario = ForeignKey(
        Cuestionario,
        on_delete=CASCADE,
        related_name='soluciones'
    )

    class Meta:
        unique_together = ('alumno', 'cuestionario',)

    def __str__(self):
        return f'Solucion {self.id}'


class SolucionPregunta(BaseModel):
    # cuando se responde la pregunta
    respuesta = CharField(
        'Respuesta',
        max_length=250,
        blank=False,
    )
    puntaje_obtenido = DecimalField(
        'Puntaje Obtenido',
        max_digits=10,
        decimal_places=2,
        blank=False,
        default=0,
    )
    intentos_tomados = IntegerField(
        'Intentos',
        blank=False,
        default=0,
    )
    comentario = CharField(
        'Comentario',
        max_length=250,
        blank=True,
        null=True,
    )
    situacion_respuesta = CharField(
        'Situacion de Respuesta',
        max_length=1,
        choices=SituacionRespuesta.choices,
        default=SituacionRespuesta.PASABLE,
    )
    solucion = ForeignKey(
        Solucion,
        on_delete=CASCADE,
        related_name='soluciones_preguntas'
    )
    cuestionario_pregunta = ForeignKey(
        CuestionarioPregunta,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    pregunta_opcion = ForeignKey(
        PreguntaOpcion,
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('solucion', 'cuestionario_pregunta',)

    def __str__(self):
        return self.respuesta
