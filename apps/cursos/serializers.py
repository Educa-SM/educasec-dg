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



#cuestionarios Banco
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

#preguntas banco
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


