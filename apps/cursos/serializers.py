from rest_framework import serializers
from .models import *


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = [
            'id',
            'nombre',
        ]

        extra_kwargs = {'id': {'read_only': True}}


class GradoSerializer(serializers.ModelSerializer):
    cursos = CursoSerializer(many=True, read_only=True)

    class Meta:
        model = Grado
        fields = [
            'id',
            'nombre',
            'cursos'
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


class CursoDocenteSerializer(serializers.ModelSerializer):
    institucion_id = serializers.PrimaryKeyRelatedField(
        queryset=Institucion.objects.all(), source='institucion')
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso')
    docente = serializers.SlugRelatedField(read_only=True, slug_field='id')
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')

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


class CursoDocenteInscripcionSerializer(serializers.ModelSerializer):
    institucion_id = serializers.PrimaryKeyRelatedField(
        queryset=Institucion.objects.all(), source='institucion')
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso')
    docente = DocenteSerializer(read_only=True)
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')

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


"""**********************   Preguntas Banco       ***************************"""


# preguntas banco
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
    id = serializers.IntegerField(required=False)
    curso = serializers.SlugRelatedField(read_only=True, slug_field='id')
    opciones = PreguntaOpcionSerializer(many=True, required=False)
    class Meta:
        model = Pregunta
        fields = [
            'id',
            'texto',
            'tipo',
            'curso',
            'opciones',
            'creation_date',
            'cuestionarios_pregunta'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'tipo': {'required': True},
            'creation_date': {'read_only': True},
            'cuestionarios_pregunta': {'read_only': True}
        }

    def create(self, validated_data):
        opciones = validated_data.pop('opciones', [])
        pregunta = Pregunta.objects.create(**validated_data)
        if validated_data['tipo'] == 'O':
            for opcion in opciones:
                PreguntaOpcion.objects.create(pregunta=pregunta, **opcion)
        return pregunta

    def update(self, instance, validated_data):
        opciones = validated_data.pop('opciones', [])
        instance.texto = validated_data.get('texto', instance.texto)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.save()
        if instance.tipo == 'O':
            for opcion in instance.opciones.all():
                if not [el for el in opciones if ('id' in el) and (el['id'] == opcion.id)]:
                    opcion.delete()
            for opcion in opciones:
                if not 'id' in opcion:
                    PreguntaOpcion.objects.create(pregunta=instance, **opcion)
                else:
                    opcion_instance = PreguntaOpcion.objects.get(
                        id=opcion['id'])
                    opcion_instance.texto = opcion['texto']
                    opcion_instance.correcta = opcion['correcta']
                    opcion_instance.save()
        return instance


"""**********************   Cuestionarios Banco       ***************************"""


# cuestonario pregunta
class CuestionarioPreguntaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    pregunta = PreguntaSerializer(required=True)

    class Meta:
        model = CuestionarioPregunta
        fields = [
            'id',
            'intentos_disponibles',
            'puntaje_asignado',
            'nombre',
            'pregunta',
            'creation_date'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'creation_date': {'read_only': True},
            'nombre': {'required': False},
        }


# cuestionarios Banco
class CuestionarioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', required=False, write_only=True)
    preguntas = CuestionarioPreguntaSerializer(many=True, required=False)

    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'curso',
            'preguntas',
            'creation_date',
            'curso_id',
            'cuestionarios_curso'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'creation_date': {'read_only': True},
            'cuestionarios_curso': {'read_only': True},
            'curso_id': {'required': False},
        }

    def create(self, validated_data):
        preguntas = validated_data.pop('preguntas', [])
        cuestionario = Cuestionario.objects.create(**validated_data)
        # pregunta del cuestionario
        for preguntaCuestion in preguntas:
            data_pregunta = preguntaCuestion.pop('pregunta', {})
            if 'id' in data_pregunta:
                pregunta = Pregunta.objects.get(id=data_pregunta['id'])
            else:
                opciones = data_pregunta.pop('opciones', [])
                pregunta = Pregunta.objects.create(
                    **data_pregunta, curso=cuestionario.curso)
                if data_pregunta['tipo'] == 'O':
                    for opcion in opciones:
                        PreguntaOpcion.objects.create(
                            pregunta=pregunta, **opcion)
            CuestionarioPregunta.objects.create(
                cuestionario=cuestionario, pregunta=pregunta, nombre=data_pregunta['texto'], **preguntaCuestion)
        return cuestionario

    def update(self, instance, validated_data):
        preguntas = validated_data.pop('preguntas', [])
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()
        # eliminar preguntasCuestionario no ha sido enviado
        for preguntaCuestion in instance.preguntas.all():
            if not [el for el in preguntas if ('id' in el) and (el['id'] == preguntaCuestion.id)]:
                #print("delete"+ preguntaCuestion.id)
                preguntaCuestion.delete()
        for preguntaCuestion in preguntas:
            # pregunta cuestionario no tiene id
            if not 'id' in preguntaCuestion:
                # PREGUNTA
                data_pregunta = preguntaCuestion.pop('pregunta', {})
                if 'id' in data_pregunta:
                    pregunta = Pregunta.objects.get(id=data_pregunta['id'])
                else:
                    opciones = data_pregunta.pop('opciones', [])
                    pregunta = Pregunta.objects.create(
                        **data_pregunta, curso=instance.curso)
                    if data_pregunta['tipo'] == 'O':
                        for opcion in opciones:
                            PreguntaOpcion.objects.create(
                                pregunta=pregunta, **opcion)
                CuestionarioPregunta.objects.create(
                    cuestionario=instance, pregunta=pregunta, nombre=data_pregunta['texto'], **preguntaCuestion)
            else:
                # PREGUNTA CUESTIONARIO tiene id
                pregunta_cuestionario_instance = CuestionarioPregunta.objects.get(
                    id=preguntaCuestion['id'])
                pregunta_cuestionario_instance.intentos_disponibles = preguntaCuestion[
                    'intentos_disponibles']
                pregunta_cuestionario_instance.puntaje_asignado = preguntaCuestion[
                    'puntaje_asignado']

                data_pregunta = preguntaCuestion.pop('pregunta', {})
                # pregunta BANCO tiene id
                if 'id' in data_pregunta:
                    pregunta = Pregunta.objects.get(id=data_pregunta['id'])
                else:
                    # pregunta BANCO no tiene id
                    opciones = data_pregunta.pop('opciones', [])
                    pregunta = Pregunta.objects.create(
                        **data_pregunta, curso=instance.curso)
                    if data_pregunta['tipo'] == 'O':
                        for opcion in opciones:
                            PreguntaOpcion.objects.create(
                                pregunta=pregunta, **opcion)
                pregunta_cuestionario_instance.pregunta = pregunta
                pregunta_cuestionario_instance.nombre = data_pregunta['texto']
                pregunta_cuestionario_instance.save()
        return instance


# ------------------     Inscripciones Cursos    ---------------------
class IncripcionCursoSerializer(serializers.ModelSerializer):
    curso_docente = CursoDocenteInscripcionSerializer(read_only=True)

    class Meta:
        model = AlumnoInscripcionCurso
        fields = [
            'id',
            'curso_docente',
            'creation_date',
            'estate',

        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
            'alumno': {'read_only': True},
        }
