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
      model  = AlumnoInscripcionCurso
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

class CursoDocenteSerializer(serializers.ModelSerializer):
   institucion_id = serializers.PrimaryKeyRelatedField( 
            queryset=Institucion.objects.all(), source='institucion')
   curso_id = serializers.PrimaryKeyRelatedField(
            queryset=Curso.objects.all(), source='curso')
   docente = serializers.SlugRelatedField( read_only=True, slug_field='id')
   curso = serializers.SlugRelatedField( read_only=True, slug_field='nombre')
   #inscripciones = IncripcionCursoDocenteSerializer(read_only=True, many=True)
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
         'docente',
         'curso',
         'creation_date'
      ]
      extra_kwargs = { 
         'id': {'read_only': True}, 
         'docente': {'read_only': True},
         'codigo_inscripcion': {'read_only': True},
         'curso': {'read_only': True},
         'creation_date': {'read_only': True}
      }


#cursos Admin para 
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
class CursoDocenteInscripcionSerializer(serializers.ModelSerializer):
   institucion_id = serializers.PrimaryKeyRelatedField( 
            queryset=Institucion.objects.all(), source='institucion')
   curso_id = serializers.PrimaryKeyRelatedField(
            queryset=Curso.objects.all(), source='curso')
   docente = DocenteSerializer(read_only=True)
   curso = serializers.SlugRelatedField( read_only=True, slug_field='nombre')
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
         'docente',
         'curso',
         'creation_date',
      ]

class IncripcionCursoSerializer(serializers.ModelSerializer):
   curso_docente = CursoDocenteInscripcionSerializer(read_only = True )
   class Meta:
      model  = AlumnoInscripcionCurso
      fields = [
         'id',
         'curso_docente',
         'creation_date',
         'estate'
      ]
      extra_kwargs = {
         'id': {'read_only': True},
         'creation_date': {'read_only': True},
         'alumno': {'read_only': True},
      }


"""**********************   Preguntas Banco       ***************************"""

#preguntas banco
class PreguntaOpcionSerializer(serializers.ModelSerializer):
   id = serializers.IntegerField(required=False)
   class Meta:
      model = PreguntaOpcion
      fields = [
         'id',
         'texto',
         'correcta'
      ]
      extra_kwargs = { 
         'id': {'required': False},
         'correcta': {'required': True} 
      }

class PreguntaSerializer(serializers.ModelSerializer):
   curso = serializers.SlugRelatedField( read_only=True, slug_field='id')
   #curso_id = serializers.PrimaryKeyRelatedField( 
   #         queryset=Curso.objects.all(), source='curso')
   opciones = PreguntaOpcionSerializer(many=True, required=False)
   class Meta:
      model = Pregunta
      fields = [
         'id',
         'texto',
         'tipo',
         'curso',
         #'curso_id',
         'opciones',
         'creation_date',
      ]

      extra_kwargs = { 
         'id': {'read_only': True},
         'tipo': {'required': True},
         'creation_date': {'read_only': True}
      }
   def create(self, validated_data):
      opciones = validated_data.pop('opciones',[])
      pregunta =  Pregunta.objects.create(**validated_data)
      if validated_data['tipo']=='O':
         for opcion in opciones:
            PreguntaOpcion.objects.create(pregunta=pregunta,**opcion)
      return pregunta
      
   def update(self, instance, validated_data):
      opciones = validated_data.pop('opciones',[])
      instance.texto = validated_data.get('texto', instance.texto)
      instance.tipo = validated_data.get('tipo', instance.tipo)
      instance.save()
      if instance.tipo=='O':
         for opcion in opciones:
            if not 'id' in opcion:
               PreguntaOpcion.objects.create(pregunta=instance,**opcion)
            else:
               opcion_instance = PreguntaOpcion.objects.get(id=opcion['id'])
               opcion_instance.texto = opcion['texto']
               opcion_instance.correcta = opcion['correcta']
               opcion_instance.save()
      return instance


"""**********************   Cuestionarios Banco       ***************************"""
# cuestonario pregunta
class CuestionarioPregunta(serializers.ModelSerializer):
   pregunta = PreguntaSerializer(read_only=True)
   pregunta_id = serializers.PrimaryKeyRelatedField( 
            queryset=Pregunta.objects.all(), source='pregunta_id')
   class Meta:
      model = CuestionarioPregunta
      fields = [
         'id',
         'intentos_disponibles',
         'puntaje_asignado',
         'numero_orden',
         'nombre',

         'pregunta',
         'pregunta_id',
         'creation_date'
      ]
      extra_kwargs = { 
         'id': {'read_only': True},
         'creation_date': {'read_only': True},
         'nombre': {'required': False},
      }

#cuestionarios Banco
class CuestionarioSerializer(serializers.ModelSerializer):
   curso = serializers.SlugRelatedField( read_only=True, slug_field='nombre')
   curso_id = serializers.PrimaryKeyRelatedField( 
            queryset=Curso.objects.all(), source='curso')
   preguntas = CuestionarioPregunta(many=True, required=False)
   class Meta:
      model = Cuestionario
      fields = [
         'id',
         'nombre',
         'curso',
         'curso_id',
         'preguntas'
      ]

      extra_kwargs = { 
         'id': {'read_only': True}
      }

   def create(self, validated_data):
      preguntas = validated_data.pop('preguntas',[])
      cuestionario =  Cuestionario.objects.create(**validated_data)
      for pregunta in preguntas:
         CuestionarioPregunta.objects.create(cuestionario=cuestionario,**pregunta)
      return cuestionario
   
   def update(self, instance, validated_data):
      preguntas = validated_data.pop('preguntas',[])
      instance.nombre = validated_data.get('nombre', instance.nombre)
      instance.curso = validated_data.get('curso', instance.curso)
      instance.save()
      for pregunta in preguntas:
         if not 'id' in pregunta:
            CuestionarioPregunta.objects.create(cuestionario=instance,**pregunta)
         else:
            pregunta_instance = CuestionarioPregunta.objects.get(id=pregunta['id'])
            pregunta_instance.intentos_disponibles = pregunta['intentos_disponibles']
            pregunta_instance.puntaje_asignado = pregunta['puntaje_asignado']
            # pregunta_instance.nombre = pregunta['nombre']
            pregunta_instance.save()
      return instance
