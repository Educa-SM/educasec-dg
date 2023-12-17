from datetime import datetime as dt
from django.db.models import (
    CharField, ImageField, DateTimeField,
    DecimalField, ForeignKey, IntegerField,TextField,
    BooleanField
)
from django.db.models.deletion import CASCADE, SET_NULL
from apps.cursos.models import Curso
from apps.institucion.models import Alumno
from educasm.utils.models import BaseModel
from .choices import *
from educasm.utils.defs import upload_to

class Cuestionario(BaseModel):
    nombre = CharField( 'Nombre', max_length=150, blank=False, null=False,)
    descripcion = TextField( 'Descripcion', blank=True, null=True,)
    imagen = ImageField( 'Imagen',
        upload_to=upload_to(
            model='cuestionario_banco',
            path=dt.today().strftime('%Y/%m/%d')
        ),
        blank=True, null=True,
    )
    fecha_asignacion = DateTimeField('Fecha de Asignacion',)
    fecha_expiracion = DateTimeField( 'Fecha de Expiracion',)
    is_banco = BooleanField( '¿pertenece al banco de preguntas?', default=False,)
    estate = CharField( 'Estado', max_length=1, choices=EstadoCuestionario.choices, default=EstadoCuestionario.ACTIVO,)

    curso = ForeignKey( Curso, on_delete=SET_NULL, null=True, blank=True, related_name='cuestionarios',)

    def __str__(self):
        return self.nombre

# *****************   Cuestionario    *******************
class Pregunta(BaseModel):
    texto = TextField( 'Detalle',blank=True, null=True)
    tipo = CharField(
        'Tipo de Pregunta',
        max_length=1,
        choices=TipoPregunta.choices,
        default=TipoPregunta.RESPUESTA_SIMPLE,
    )
    imagen = ImageField(
        'Imagen',
        upload_to=upload_to(model='pregunta', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True,
    )
    intentos_disponibles = IntegerField( null=False, default=1,)
    puntaje_asignado = DecimalField( null=False, max_digits=12, decimal_places=2, default=0.0,)
    nombre = CharField( 'Nombre', max_length=150, blank=True, null=True, )
    is_banco = BooleanField( '¿pertenece al banco de preguntas?', default=False,)
    estate = CharField( 'Estado', max_length=1, choices=EstadoPregunta.choices, default=EstadoPregunta.ACTIVO,)

    cuestionario = ForeignKey( Cuestionario, on_delete=SET_NULL,
        related_name='preguntas', blank=True, null=True )

    def __str__(self):
        return self.texto


class OpcionPregunta(BaseModel):
    texto = CharField( max_length=300, null=False,)
    correcta = CharField( '¿Es correcta?', max_length=1,
        choices=SituacionPregunta.choices, default=SituacionPregunta.INCORRECTA,)
    pregunta = ForeignKey( Pregunta, on_delete=CASCADE, related_name='opciones',)
    estate = CharField( 'Estado', max_length=1, choices=EstadoOpcionPregunta.choices, default=EstadoOpcionPregunta.ACTIVO,)

    def __str__(self):
        return self.texto



class Solucion(BaseModel):
    fecha_solucion = DateTimeField( 'Fecha de Solucion', auto_now_add=True,)
    fecha_revision = DateTimeField( 'Fecha Revision', blank=True, null=True,)
    comentario = CharField( 'Comentario', max_length=250, blank=True, null=True, )
    alumno = ForeignKey( Alumno, on_delete=CASCADE, )
    cuestionario = ForeignKey( Cuestionario, on_delete=CASCADE, related_name='soluciones')

    estate = CharField( 'Estado', max_length=1, choices=EstadoSolucion.choices, default=EstadoSolucion.ACTIVO,)

    class Meta:
        unique_together = ('alumno', 'cuestionario',)

    def __str__(self):
        return f'Solucion {self.id}'


class SolucionPregunta(BaseModel):
    # cuando se responde la pregunta
    respuesta = CharField( 'Respuesta', max_length=500, blank=False,)
    puntaje_obtenido = DecimalField( 'Puntaje Obtenido', max_digits=10, decimal_places=2, blank=False, default=0, )
    intentos_tomados = IntegerField( 'Intentos', blank=False, default=0, )
    comentario = CharField( 'Comentario', max_length=500, blank=True, null=True,)
    situacion_respuesta = CharField( 'Situacion de Respuesta', max_length=1, choices=SituacionRespuesta.choices, default=SituacionRespuesta.PASABLE,)
    estate = CharField( 'Estado', max_length=1, choices=EstadoSolucionPregunta.choices, default=EstadoSolucionPregunta.ACTIVO, )

    solucion = ForeignKey( Solucion, on_delete=CASCADE, related_name='soluciones_preguntas')
    pregunta = ForeignKey( Pregunta, on_delete=SET_NULL, null=True, blank=True,)
    pregunta_opcion = ForeignKey( OpcionPregunta, on_delete=SET_NULL, null=True, blank=True,)

    class Meta:
        unique_together = ('solucion', 'pregunta',)

    def __str__(self):
        return self.respuesta
