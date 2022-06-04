from django.db.models import CharField, ManyToManyField, OneToOneField
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from apps.seguridad.models import User
from educasec.utils.models import BaseModel
from .choices import TipoDocIdentidad


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
