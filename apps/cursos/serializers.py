from rest_framework import serializers

from .models import *
class CursoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Curso
      fields = [
         'id',
         'nombre',
      ]

      extra_kwargs = { 'id': {'read_only': True} }

class GradoSerializer(serializers.ModelSerializer):
   cursos = CursoSerializer(many = True, read_only = True )
   class Meta:
      model = Grado
      fields = [
         'id',
         'nombre',
         'cursos'
      ]
      extra_kwargs = { 'id': {'read_only': True} }

class NivelSerializer(serializers.ModelSerializer):
   grados = GradoSerializer(many = True, read_only = True )
   class Meta:
      model = Nivel
      fields = [
         'id',
         'nombre',
         'grados'
      ]
      extra_kwargs = { 'id': {'read_only': True} }





class CursoDocenteSerializer(serializers.ModelSerializer):
   institucion_id = serializers.PrimaryKeyRelatedField( 
            queryset=Institucion.objects.all(), source='institucion')
   curso_id = serializers.PrimaryKeyRelatedField( 
            queryset=Curso.objects.all(), source='curso')
   docente_id = serializers.PrimaryKeyRelatedField( 
            queryset=Docente.objects.all(), source='docente')
   class Meta:
      model = CursoDocente
      fields = [
         'id',
         'nombre',
         'periodo',
         'year',
         'codigo_inscripcion',
         'institucion_id',
         'curso_id',
         'docente_id'
      ]
      extra_kwargs = { 'id': {'read_only': True} }

class CuestionarioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Cuestionario
      fields = [
         'id',
         'nombre',
         'fecha_disponible',
         'fecha_expiracion',
         'docente',
         'curso'
      ]

      extra_kwargs = { 'id': {'read_only': True} }

class PreguntaSerializer(serializers.ModelSerializer):
   class Meta:
      model = Pregunta
      fields = [
         'texto',
         'tipo',
         'docente',
         'curso',
      ]

      extra_kwargs = { 'id': {'read_only': True} }


