from datetime import datetime as dt
from django.db.models import CharField, FileField, ForeignKey, ImageField, URLField, TextField
from django.db.models.deletion import CASCADE
from django.forms import model_to_dict
from apps.institucion.models import Institucion
from apps.recursos.choices import *
from educasm.utils.defs import upload_to
from educasm.utils.models import BaseModel


class Recurso(BaseModel):
    titulo = CharField( 'Título', max_length=500, default='', blank=False, null=False,)
    descripcion = TextField( 'Descripción', blank=False, null=False,)
    contenido = CharField( 'Contenido', max_length=500, blank=True, null=True,)
    tipo = CharField( 'Tipo', max_length=1, choices=TipoRecursoChoices.choices, blank=False, null=False,)
    institucion = ForeignKey( Institucion, on_delete=CASCADE, blank=True, null=True,)
    original_filename = FileField(
        'Archivo Original',
        upload_to=upload_to(
            model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True
    )
    miniatura = ImageField(
        'Miniatura',
        upload_to=upload_to(
            model='recurso', path=dt.today().strftime('%Y/%m/%d')),
        blank=False,
        null=False,
    )

    estate = CharField( 'Estado', max_length=1, choices=EstadoRecurso.choices, default=EstadoRecurso.ACTIVO,)

    def __str__(self):
        return self.titulo

    def to_dict(self):
        dict = model_to_dict(
            self, exclude=['original_filename', 'miniatura'])
        dict['tipo'] = TipoRecursoChoices(self.tipo).to_dict()
        dict['miniatura'] = self.miniatura.url
        if self.original_filename:
            dict['original_filename'] = self.original_filename.url
        return dict


class TipoJuego(BaseModel):
    nombre = CharField( 'Nombre', max_length=100, null=False, unique=True, )
    estate = CharField( 'Estado', max_length=1, choices=EstadoTipoJuego.choices, default=EstadoTipoJuego.ACTIVO,)

    def __str__(self):
        return self.nombre


class Juego(BaseModel):
    texto = CharField( 'Texto', max_length=255, null=True, blank=True, )
    recurso = ForeignKey( Recurso, on_delete=CASCADE, )
    tipo_juego = ForeignKey( TipoJuego, on_delete=CASCADE, )
    estate = CharField( 'Estado', max_length=1, choices=EstadoJuego.choices, default=EstadoJuego.ACTIVO,)

    def __str__(self):
        return self.texto


class OpcionJuego(BaseModel):
    pregunta = CharField(
        'Pregunta',
        blank=True,
        null=True,
        max_length=255,
    )
    texto = CharField(
        'Texto',
        max_length=255,
        blank=False,
        null=False,
    )
    juego = ForeignKey(
        Juego,
        on_delete=CASCADE,
    )
    estate =  CharField( 'Estado', max_length=1, choices=EstadoOpcionJuego.choices, default=EstadoOpcionJuego.ACTIVO,)
    def __str__(self):
        return self.texto


class Patrocinador(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
    )
    descripcion = CharField(
        'Descripción',
        max_length=150,
        blank=True,
        null=True,
    )
    telefono = CharField(
        'Teléfono',
        max_length=50,
        blank=True,
        null=True,
    )
    facebook = URLField(
        'Facebook',
        max_length=100,
        blank=True,
        null=True,
    )
    email = CharField(
        'Email',
        max_length=100,
        blank=True,
        null=True,
    )
    web = URLField(
        'Web',
        max_length=100,
        blank=True,
        null=True,
    )
    logo = ImageField(
        'Logo',
        upload_to=upload_to(
            model='patrocinador', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True,
    )
    estate = CharField( 'Estado', max_length=1, choices=EstadoPatrocinador.choices, default=EstadoPatrocinador.ACTIVO,)
    def __str__(self):
        return self.nombre


class MiembroProyecto(BaseModel):
    nombre = CharField(
        'Nombre',
        max_length=150,
        blank=False,
        null=False,
        unique=True,
    )
    descripcion = CharField(
        'Descripción',
        max_length=150,
        blank=True,
        null=True,
    )
    cargo = CharField(
        'Cargo',
        max_length=20,
        blank=True,
        null=True,
    )
    logo = ImageField(
        'Logo',
        upload_to=upload_to(
            model='miembro_proyecto', path=dt.today().strftime('%Y/%m/%d')),
        blank=True,
        null=True,
    )

    estate = CharField( 'Estado', max_length=1, choices=EstadoMiembroProyecto.choices, default=EstadoMiembroProyecto.ACTIVO,)

    def __str__(self):
        return self.nombre
