from rest_framework import serializers
from .models import *


class TipoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCurso
        fields = [
            'id',
            'nombre',
        ]

        extra_kwargs = {'id': {'read_only': True}}


class GradoSerializer(serializers.ModelSerializer):
    tipos_cursos = TipoCursoSerializer(many=True, read_only=True)

    class Meta:
        model = Grado
        fields = [
            'id',
            'nombre',
            'tipos_cursos'
        ]
        extra_kwargs = {'id': {'read_only': True}}


class NivelSerializer(serializers.ModelSerializer):
    grados = GradoSerializer(many=True, read_only=True)

    class Meta:
        model = Nivel
        fields = [
            'id',
            'nombre',
            'grados'
        ]
        extra_kwargs = {'id': {'read_only': True}}


# cursos Admin para docentes
class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = [
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'nro_documento',
            'tipo_documento'
        ]


class IncripcionCursoDocenteSerializer(serializers.ModelSerializer):
    alumno = AlumnoSerializer(read_only=True)

    class Meta:
        model = AlumnoInscripcionCurso
        fields = [
            'id',
            'creation_date',
            'alumno',
            'estate'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
        }


class CursoSerializer(serializers.ModelSerializer):
    institucion_id = serializers.PrimaryKeyRelatedField(
        queryset=Institucion.objects.all(), source='institucion')
    tipo_curso_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoCurso.objects.all(), source='tipo_curso')
    docente = serializers.SlugRelatedField(read_only=True, slug_field='id')
    tipo_curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')

    cuestionarios = serializers.SlugRelatedField(read_only=True, slug_field='id', many=True)

    inscripciones = serializers.SlugRelatedField(read_only=True, slug_field='id', many=True)

    class Meta:
        model = Curso
        fields = [
            'id',
            'nombre',
            'periodo',
            'year',
            'codigo_inscripcion',
            'institucion_id',
            'tipo_curso_id',
            'docente',
            'tipo_curso',
            'creation_date',
            'cuestionarios',
            'inscripciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'docente': {'read_only': True},
            'codigo_inscripcion': {'read_only': True},
            'tipo_curso': {'read_only': True},
            'creation_date': {'read_only': True},
            'cuestionarios': {'read_only': True},
            'inscripciones': {'read_only': True},
        }


# cursos Admin para
class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = [
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'nro_documento',
            'tipo_documento'
        ]


class CursoInscripcionSerializer(serializers.ModelSerializer):
    institucion_id = serializers.PrimaryKeyRelatedField(
        queryset=Institucion.objects.all(), source='institucion')
    tipo_curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='tipo_curso')
    docente = DocenteSerializer(read_only=True)
    tipo_curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    institucion = serializers.SlugRelatedField(read_only=True, slug_field='nombre')

    class Meta:
        model = Curso
        fields = [
            'id',
            'nombre',
            'periodo',
            'year',
            'codigo_inscripcion',
            'institucion_id',
            'institucion',
            'tipo_curso_id',
            'docente',
            'tipo_curso',
            'creation_date',
        ]
        extra_kwargs = {
            'institucion': {'read_only': True},
        }


# ------------------     Inscripciones Cursos    ---------------------
class IncripcionCursoSerializer(serializers.ModelSerializer):
    curso = CursoInscripcionSerializer(read_only=True)

    class Meta:
        model = AlumnoInscripcionCurso
        fields = [
            'id',
            'curso',
            'creation_date',
            'estate',

        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
            'alumno': {'read_only': True},
        }
