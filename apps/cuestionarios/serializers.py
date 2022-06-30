from rest_framework.serializers import ModelSerializer, SlugRelatedField
from apps.cursos.serializers import *
from .models import *


class CuestionarioCursoSerializer(ModelSerializer):
    curso_docente = SlugRelatedField(read_only=True, slug_field='nombre')
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
            'creation_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
        }

    def create(self, validated_data):
        data_cuestionario = validated_data.pop('cuestionario')
        # cuestionario create
        if 'id' in data_cuestionario:
            cuestionario = Cuestionario.objects.get(id=data_cuestionario['id'])
        else:
            preguntas = data_cuestionario.pop('preguntas', [])
            cuestionario = Cuestionario.objects.create(**data_cuestionario)
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
        return CuestionarioCurso.objects.create(cuestionario=cuestionario, **validated_data)


class CuestionarioCursoAlumnoSerializer(ModelSerializer):
    curso_docente = SlugRelatedField(read_only=True, slug_field='nombre')

    class Meta:
        model = CuestionarioCurso
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso_docente',
            'creation_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
        }
