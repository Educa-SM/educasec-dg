from rest_framework import serializers

from .models import Cuestionario, Curso, Grado, Nivel, Pregunta

class GradoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Grado
      fields = [
         'id',
         'nombre',
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



class CursoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Curso
      fields = [
         'id',
         'nombre',
         'nivel',
         'institucion',
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


