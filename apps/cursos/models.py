
from django.db.models import CharField, ForeignKey, IntegerField
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.translation import gettext_lazy as _
from apps.institucion.models import Alumno, Docente, Institucion
from educasm.utils.models import BaseModel


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



# ******************  Inscripcion de Cursos   *********************
class Curso(BaseModel):
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
    grado = ForeignKey(
        Grado,
        on_delete=SET_NULL,
        blank=True,
        null=True
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
        self.codigo_inscripcion = (self.nombre[0] + self.grado.nombre[0] +
                                   self.docente.nombres[0]+self.institucion.nombre[0] +
                                   str(Curso.objects.count()+1))
        super(Curso, self).save(**kwargs)


# la inscripcion -> estado=1(registrado)   estado=2
class AlumnoInscripcionCurso(BaseModel):
    alumno = ForeignKey(
        Alumno,
        on_delete=CASCADE,
    )
    curso = ForeignKey(
        Curso,
        on_delete=CASCADE,
        related_name='inscripciones',
    )

    class Meta:
        unique_together = ('alumno', 'curso',)
