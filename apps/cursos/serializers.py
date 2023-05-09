from rest_framework import serializers
from .models import *

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = [
            'id',
            'nombre',
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
    grado_id = serializers.PrimaryKeyRelatedField(
        queryset=Grado.objects.all(), source='grado', required=False)
    docente = serializers.SlugRelatedField(read_only=True, slug_field='id')
    grado = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
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
            'grado_id',
            'docente',
            'grado',
            'creation_date',
            'cuestionarios',
            'inscripciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'docente': {'read_only': True},
            'codigo_inscripcion': {'read_only': True},
            'grado': {'read_only': True},
            'grado_id': {'required': False},
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
    grado_id = serializers.PrimaryKeyRelatedField(
        queryset=Grado.objects.all(), source='grado')
    docente = DocenteSerializer(read_only=True)
    grado = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
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
            'grado_id',
            'docente',
            'grado',
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
