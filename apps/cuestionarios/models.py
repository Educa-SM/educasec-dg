from django.db.models import CharField, DateTimeField, DecimalField, ForeignKey, IntegerField
from django.db.models.deletion import CASCADE, SET_NULL
from apps.cursos.models import Cuestionario, CuestionarioPregunta, CursoDocente, PreguntaOpcion
from apps.institucion.models import Alumno
from educasec.utils.models import BaseModel
from .choices import SituacionRespuesta


class CuestionarioCurso(BaseModel):
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
    curso_docente = ForeignKey(
        CursoDocente,
        on_delete=CASCADE,
    )
    cuestionario = ForeignKey(
        Cuestionario,
        on_delete=CASCADE,
        related_name='cuestionarios_curso'
    )

    def __str__(self):
        return self.nombre


class SolucionCuestionario(BaseModel):
    fecha_solucion = DateTimeField(
        'Fecha de Solucion',
    )
    fecha_revision = DateTimeField(
        'Apellido Paterno',
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
    cuestionario_curso = ForeignKey(
        CuestionarioCurso,
        on_delete=CASCADE,
    )

    class Meta:
        unique_together = ('alumno', 'cuestionario_curso',)

    def __str__(self):
        return f'SolucionCuestionario {self.id}'


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
        SolucionCuestionario,
        on_delete=CASCADE,
    )
    cuestionario_pregunta = ForeignKey(
        CuestionarioPregunta,
        on_delete=CASCADE,
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
