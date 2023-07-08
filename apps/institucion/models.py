from datetime import datetime as dt
from django.db.models import (
    CharField, ManyToManyField, OneToOneField, TextField, ForeignKey,
    DateField,ImageField
)
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.translation import gettext_lazy as _
from apps.seguridad.models import User
from educasm.utils.models import BaseModel
from .choices import TipoDocIdentidad
from educasm.utils.defs import upload_to

class Institucion(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=255,
        null=False,
        blank=False,
    )
    direccion = CharField(
        'Direccion',
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class Docente(BaseModel):
    nombres = CharField(
        'Nombres',
        max_length=150,
        null=False,
        blank=False,
    )
    apellido_paterno = CharField(
        'Apellido Paterno',
        max_length=150,
        null=False,
        blank=False,
    )
    apellido_materno = CharField(
        'Apellido Materno',
        max_length=150,
        null=False,
        blank=False,
    )
    direccion = CharField(
        'Direccion',
        max_length=255,
        blank=True,
        null=True,
    )
    tipo_documento = CharField(
        'Tipo de Documento',
        max_length=3,
        choices=TipoDocIdentidad.choices,
        default=TipoDocIdentidad.DNI,
    )
    nro_documento = CharField(
        'Numero de Documento de Identidad',
        unique=True,
        max_length=12,
    )

    user = OneToOneField(
        User,
        on_delete=CASCADE,
    )
    instituciones = ManyToManyField(
        Institucion,
    )

    def __str__(self):
        return self.nombres + ' '+self.apellido_paterno+' '+self.apellido_materno


class Alumno(BaseModel):
    nro_documento = CharField(
        'Numero de Documento de Identidad',
        unique=True,
        max_length=12,
    )
    nombres = CharField(
        'Nombres',
        max_length=150,
        blank=False,
    )
    apellido_paterno = CharField(
        'Apellido Paterno',
        max_length=150,
        blank=False,
    )
    apellido_materno = CharField(
        'Apellido Materno',
        max_length=150,
        blank=False,
    )
    tipo_documento = CharField(
        'Tipo de Documento',
        max_length=3,
        choices=TipoDocIdentidad.choices,
        default=TipoDocIdentidad.DNI,
    )
    user = OneToOneField(
        User,
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.nombres + ' '+self.apellido_paterno+' '+self.apellido_materno

class MensajeInicio(BaseModel):
    titulo = CharField(
        'Titulo',
        max_length=255,
        null=False,
        blank=False,
    )
    descripcion = TextField(
        'Descripcion',
        null=True, blank=True
    )
    fecha_inicio = DateField(
        'Fecha de Inicio',
        null=False,
        blank=False,
    )
    fecha_fin = DateField(
        'Fecha de Fin',
        null=False,
        blank=False,
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

    docente = ForeignKey( Docente, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.titulo