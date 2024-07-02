from rest_framework import serializers
from apps.cursos.serializers import *
from .models import *


"""**********************  OPCION PREGUNTA       ***************************"""
# Opcion Pregunta
class OpcionPreguntaListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = OpcionPregunta
        fields = [
            'id',
            'texto',
            'correcta'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'correcta': {'required': False}
        }

class OpcionPreguntaAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionPregunta
        fields = [
            'id',
            'texto'
        ]
        extra_kwargs = {
            'id': {'required': False},
        }


## para creacion y actualizacion
class PreguntaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    #tipo_curso = serializers.SlugRelatedField(read_only=True, slug_field='id')
    opciones = OpcionPreguntaListSerializer(many=True, required=False)
    cuestionario_nombre = serializers.SlugRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario', slug_field='nombre', required=False)
    cuestionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario', required=False)

    class Meta:
        model = Pregunta
        fields = [
            'id',
            'texto',
            'tipo',
            'intentos_disponibles',
            'puntaje_asignado',
            'nombre',
            'opciones',
            'cuestionario_nombre',
            'cuestionario_id',
            'creation_date',
            'is_banco',
            'imagen'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'tipo': {'required': True},
            'nombre': {'required': False},
            'creation_date': {'read_only': True},
            'cuestionario_nombre': {'read_only': True, 'required': False},
            'is_banco': {'required': False},
            'cuestionario_id': {'required': False},
            'imagen': {'read_only': True},
        }

    def create(self, validated_data):
        opciones = validated_data.pop('opciones', [])
        pregunta = Pregunta.objects.create(**validated_data)
        if validated_data['tipo'] == 'O':
            for opcion in opciones:
                OpcionPregunta.objects.create(pregunta=pregunta, **opcion)
        return pregunta

    def update(self, instance, validated_data):
        opciones = validated_data.pop('opciones', [])
        instance.texto = validated_data.get('texto', instance.texto)
        #instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.intentos_disponibles = validated_data.get('intentos_disponibles', instance.intentos_disponibles)
        instance.puntaje_asignado = validated_data.get('puntaje_asignado', instance.puntaje_asignado)
        instance.nombre = validated_data.get('nombre', instance.tipo)
        instance.is_banco = validated_data.get('is_banco', instance.is_banco)
        instance.save()
        if instance.tipo == 'O':
            for opcion in instance.opciones.all():
                if not [el for el in opciones if ('id' in el) and (el['id'] == opcion.id)]:
                    opcion.delete()
            for opcion in opciones:
                if not 'id' in opcion:
                    OpcionPregunta.objects.create(pregunta=instance, **opcion)
                else:
                    opcion_instance = OpcionPregunta.objects.get(
                        id=opcion['id'])
                    opcion_instance.texto = opcion['texto']
                    opcion_instance.correcta = opcion['correcta']
                    opcion_instance.save()
        return instance

class PreguntaAlumnoSerializer(serializers.ModelSerializer):
    opciones = OpcionPreguntaAlumnoSerializer(many=True, required=False)
    class Meta:
        model = Pregunta
        fields = [
            'id',
            'texto',
            'tipo',
            'intentos_disponibles',
            'puntaje_asignado',
            'nombre',
            'opciones',
            'imagen'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'texto': {'required': False},
            'opciones': {'required': False},
            'imagen': {'read_only': True},
        }


"""**********************   Cuestionarios       ***************************"""
# cuestionarios Banco

class CuestionarioListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre',  required=False)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', required=False)
    institucion_id = serializers.SlugRelatedField(
        queryset=Curso.objects.all(), source='curso.institucion', slug_field='id', required=False)

    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso',
            'curso_id',
            'preguntas',
            'creation_date',
            'imagen',
            'institucion_id'
        ]

class CuestionarioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre',  required=False)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', required=False)
    institucion_id = serializers.SlugRelatedField(
        queryset=Curso.objects.all(), source='curso.institucion', slug_field='id', required=False)
    preguntas = PreguntaSerializer(many=True, required=False)

    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'descripcion',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso',
            'curso_id',
            'preguntas',
            'creation_date',
            'imagen',
            'institucion_id'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'creation_date': {'read_only': True},
            'curso_id': {'required': False,},
            'curso': {'required': False,'read_only': True},
            'imagen': {'read_only': True},
            'institucion_id': {'read_only': True},
            'preguntas': {'required': False},
        }

    def create(self, validated_data):
        preguntas = validated_data.pop('preguntas', [])
        cuestionario = Cuestionario.objects.create(**validated_data)
        # pregunta del cuestionario
        """for pregunta in preguntas:
            if 'id' in pregunta:
                data_pregunta = Pregunta.objects.get(id=pregunta['id'])
            else:
                preguntaSerializer = PreguntaSerializer(pregunta)
                data_pregunta = preguntaSerializer.create(pregunta)
            cuestionario.preguntas.add(data_pregunta)"""
        return cuestionario

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.nombre)
        instance.fecha_asignacion = validated_data.get('fecha_asignacion', instance.fecha_asignacion)
        instance.fecha_expiracion = validated_data.get('fecha_expiracion', instance.fecha_expiracion)
        instance.save()
        return instance


# cuestonario pregunta
class CuestionarioAlumnoSerializer(serializers.ModelSerializer):
    curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso',
            'creation_date',
            'imagen',
            'descripcion'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
            'imagen': {'read_only': True},
        }


"""
Solucion de cuestionarios por parte del alumno
"""
class SolucionPreguntaSerializer(serializers.ModelSerializer):
    pregunta_id = serializers.PrimaryKeyRelatedField(
                                queryset=Pregunta.objects.all(), 
                                source='pregunta',
                                write_only=True)
    pregunta = PreguntaSerializer(read_only=True)
    opcion_pregunta_id = serializers.PrimaryKeyRelatedField(
                                queryset=OpcionPregunta.objects.all(), 
                                source='opcion_pregunta', required=False)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = SolucionPregunta
        fields = [
            'id',
            'respuesta',  # string
            'intentos_tomados',
            'pregunta_id',
            'pregunta',
            'opcion_pregunta_id',
            'puntaje_obtenido',
            'comentario',
            'situacion_respuesta'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'comentario': {'required': False},
            'puntaje_obtenido': {'required': False},
            'opcion_pregunta_id': {'required': False},
            'pregunta_id':{'write_only':True},
            'pregunta':{'read_only':True},
        }




class SolucionDocenteSerializer(serializers.ModelSerializer):
    cuestionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario')
    soluciones_preguntas = SolucionPreguntaSerializer(many=True)
    alumno = AlumnoSerializer(read_only=True)

    class Meta:
        model = Solucion
        fields = [
            'id',
            'comentario',
            'cuestionario_id',
            'soluciones_preguntas',
            'alumno',
            'fecha_solucion',
            'fecha_revision'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'comentario': {'required': False},
            'fecha_solucion': {'read_only': True},
        }

    def update(self, instance, validated_data):
        soluciones = validated_data.pop('soluciones_preguntas', [])
        instance.comentario = validated_data.get('comentario', instance.comentario)
        instance.estate = EstadoSolucion.REVISADA
        instance.fecha_revision = dt.now()
        
        for pregunta in soluciones:
            if 'id' in pregunta:
                pregunta_instance = SolucionPregunta.objects.get(
                    id=pregunta['id'])
                pregunta_instance.puntaje_obtenido = pregunta['puntaje_obtenido']
                pregunta_instance.situacion_respuesta = pregunta['situacion_respuesta']
                pregunta_instance.save()
        instance.save()
        return instance



class SolucionSerializer(serializers.ModelSerializer):
    cuestionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario')
    soluciones_preguntas = SolucionPreguntaSerializer(many=True)
    cuestionario = CuestionarioAlumnoSerializer(required=False, many=False)
    class Meta:
        model = Solucion
        fields = [
            'id',
            'comentario',
            'cuestionario_id',
            'soluciones_preguntas',
            'fecha_solucion',
            'fecha_revision',
            'cuestionario',
            'estate'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'is_revisado': {'read_only': True},
            'comentario': {'required': False},
            'fecha_solucion': {'read_only': True},
            'fecha_revision': {'read_only': True},
            'cuestionario': {'read_only': True},
            'estate': {'read_only': True},
        }

    def create(self, validated_data):
        soluciones = validated_data.pop('soluciones_preguntas', [])
        solucion = Solucion.objects.create(**validated_data)
        for opcion in soluciones:
            # ver soluciones
            pregunta = opcion['pregunta']
            if pregunta.tipo=='O' and opcion['situacion_respuesta']=='B':
                opcion['puntaje_obtenido'] = pregunta.puntaje_asignado
            SolucionPregunta.objects.create(solucion=solucion, **opcion)
        return solucion
    
# no utilizada
class IniciarEvalucionSerializar(serializers.ModelSerializer):
    cuestionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario')
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Solucion
        fields = [
            'id',
            'cuestionario_id',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class SolucionAlumnoPreguntaSerializer(serializers.ModelSerializer):
    pregunta_id = serializers.PrimaryKeyRelatedField(
            queryset=Pregunta.objects.all(), source='pregunta')
    solucion_id = serializers.PrimaryKeyRelatedField(
            queryset=Solucion.objects.all(), source='solucion')
    opcion_pregunta_id = serializers.PrimaryKeyRelatedField( queryset=OpcionPregunta.objects.all(), 
            source='opcion_pregunta', required=False)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = SolucionPregunta
        fields = [
            'id',
            'respuesta',  
            'comentario',
            'solucion_id',
            'pregunta_id',
            'opcion_pregunta_id',
        ]
        extra_kwargs = {
            'id': {'read_only': False},
            'opcion_pregunta_id': {'required': False},
            'comentario': {'required': True},
            'respuesta': {'required': True},
            
        }