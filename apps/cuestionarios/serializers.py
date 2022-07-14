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
            'soluciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
            'soluciones': {'read_only': True},
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
    #soluciones = SlugRelatedField(many=True, read_only=True, slug_field='id')
    class Meta:
        model = CuestionarioCurso
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso_docente',
            'creation_date',
            #'soluciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
        }

"""
Solucion de cuestionarios por parte del alumno
"""
class PreguntaSolucionSerializer(ModelSerializer):
    cuestionario_pregunta_id = serializers.PrimaryKeyRelatedField(
        queryset=CuestionarioPregunta.objects.all(), source='cuestionario_pregunta')
    pregunta_opcion_id = serializers.PrimaryKeyRelatedField(
        queryset=PreguntaOpcion.objects.all(), source='pregunta_opcion', required=False)
    
    class Meta:
        model = SolucionPregunta
        fields = [
            'id',
            'respuesta', #string
            'intentos_tomados',
            'cuestionario_pregunta_id',
            'pregunta_opcion_id',
            'puntaje_obtenido',
            'comentario',
            'situacion_respuesta'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'comentario': {'required': False},
            'puntaje_obtenido': {'required': False},
            'pregunta_opcion_id': {'required': False},
        }

class SolucionSerializer(ModelSerializer):
    cuestionario_curso_id = serializers.PrimaryKeyRelatedField(
        queryset=CuestionarioCurso.objects.all(), source='cuestionario_curso')
    soluciones = PreguntaSolucionSerializer(many=True)
    class Meta:
        model = SolucionCuestionario
        fields = [
            'id',
            'comentario',
            'cuestionario_curso_id',
            'soluciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'comentario': {'required': False}
        }
    
    def create(self, validated_data):
        soluciones = validated_data.pop('soluciones', [])
        solucion = SolucionCuestionario.objects.create(**validated_data)
        for opcion in soluciones:
            
            SolucionPregunta.objects.create(solucion=solucion, **opcion)

        return solucion