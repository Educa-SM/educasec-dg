from rest_framework import serializers

from apps.cursos.serializers import *

from .models import *


class CuestionarioCursoSerializer(serializers.ModelSerializer):
   curso_docente = serializers.SlugRelatedField( read_only=True, slug_field='nombre')
   cuestionario = CuestionarioSerializer(required=True)
   class Meta:
      model = CuestionarioCurso
      fields = [
         'id', 
         'nombre',
         'fecha_asignacion',
         'fecha_expiracion',
         'cuestionario',
         'curso_docente',
         'creation_date'
      ]
      extra_kwargs = { 
         'id': {'read_only': True},
         'creation_date': {'read_only': True}
      }
   def create(self, validated_data):
      data_cuestionario = validated_data.pop('cuestionario')
      # cuestionario create
      if 'id' in data_cuestionario:
         cuestionario = Cuestionario.objects.get(id=data_cuestionario['id'])
      else:
         preguntas = validated_data.pop('preguntas',[])
         cuestionario =  Cuestionario.objects.create(**validated_data)
         #pregunta del cuestionario
         for preguntaCuestion in preguntas:
            data_pregunta = preguntaCuestion.pop('pregunta',{})
            if 'id' in data_pregunta:
               pregunta = Pregunta.objects.get(id=data_pregunta['id'])
            else:
               opciones = data_pregunta.pop('opciones',[])
               pregunta =  Pregunta.objects.create(**data_pregunta, curso=cuestionario.curso)
               if data_pregunta['tipo']=='O':
                  for opcion in opciones:
                     PreguntaOpcion.objects.create(pregunta=pregunta,**opcion)
            CuestionarioPregunta.objects.create(cuestionario=cuestionario,pregunta=pregunta,nombre=data_pregunta['texto'], **preguntaCuestion)
      return CuestionarioCurso.objects.create(cuestionario=cuestionario, **validated_data)