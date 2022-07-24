from rest_framework.serializers import ModelSerializer, SlugRelatedField
from apps.cursos.serializers import *
from .models import *

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

class PreguntaBancoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tipo_curso = serializers.SlugRelatedField(read_only=True, slug_field='id')
    opciones = PreguntaOpcionSerializer(many=True, required=False)
    class Meta:
        model = PreguntaBanco
        fields = [
            'id',
            'texto',
            'tipo',
            'tipo_curso',
            'opciones',
            'creation_date'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'tipo': {'required': True},
            'creation_date': {'read_only': True}
        }

    def create(self, validated_data):
        opciones = validated_data.pop('opciones', [])
        pregunta_banco = PreguntaBanco.objects.create(**validated_data)
        if validated_data['tipo'] == 'O':
            for opcion in opciones:
                PreguntaOpcion.objects.create(pregunta_banco=pregunta_banco, **opcion)
        return pregunta_banco

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
                    PreguntaOpcion.objects.create(pregunta_banco=instance, **opcion)
                else:
                    opcion_instance = PreguntaOpcion.objects.get(
                        id=opcion['id'])
                    opcion_instance.texto = opcion['texto']
                    opcion_instance.correcta = opcion['correcta']
                    opcion_instance.save()
        return instance


"""**********************   Cuestionarios Banco       ***************************"""

# cuestionarios Banco
class CuestionarioBancoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tipo_curso = serializers.SlugRelatedField(read_only=True, slug_field='nombre')
    tipo_curso_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoCurso.objects.all(), source='tipo_curso', required=False, write_only=True)
    preguntas_banco = PreguntaBancoSerializer(many=True, required=False)

    class Meta:
        model = CuestionarioBanco
        fields = [
            'id',
            'nombre',
            'tipo_curso',
            'preguntas_banco',
            'creation_date',
            'tipo_curso_id',
            'cuestionarios'
        ]

        extra_kwargs = {
            'id': {'required': False},
            'creation_date': {'read_only': True},
            'cuestionarios': {'read_only': True},
            'tipo_curso_id': {'required': False},
        }

    def create(self, validated_data):
        preguntas = validated_data.pop('preguntas_banco', [])
        cuestionario = CuestionarioBanco.objects.create(**validated_data)
        # pregunta del cuestionario
        for pregunta in preguntas:
            if 'id' in pregunta:
                data_pregunta = PreguntaBanco.objects.get(id=pregunta['id'])
            else:
                opciones = pregunta.pop('opciones', [])
                data_pregunta = PreguntaBanco.objects.create(
                    **pregunta, tipo_curso=cuestionario.tipo_curso)
                if pregunta['tipo'] == 'O':
                    for opcion in opciones:
                        PreguntaOpcion.objects.create(
                            pregunta_banco=data_pregunta, **opcion)
            cuestionario.preguntas_banco.add(data_pregunta)
        return cuestionario

    def update(self, instance, validated_data):
        preguntas = validated_data.pop('preguntas_banco', [])
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.save()
        # eliminar preguntasCuestionario no ha sido enviado
        for pregunta_banco in instance.preguntas_banco.all():
            if not [el for el in preguntas if ('id' in el) and (el['id'] == pregunta_banco.id)]:
                instance.preguntas_banco.remove(pregunta_banco)
                #pregunta_banco.delete()
        for pregunta_banco in preguntas:
            # pregunta cuestionario no tiene id
            if not 'id' in pregunta_banco:
                # PREGUNTA
                opciones = pregunta_banco.pop('opciones', [])
                pregunta = PreguntaBanco.objects.create(
                    **pregunta_banco, tipo_curso=instance.tipo_curso)
                if pregunta_banco['tipo'] == 'O':
                    for opcion in opciones:
                        PreguntaOpcion.objects.create(
                            pregunta_banco=pregunta, **opcion)
                instance.preguntas_banco.add(pregunta)
            else:
                # PREGUNTA CUESTIONARIO tiene id
                pregunta_instance = PreguntaBanco.objects.get(
                    id=pregunta_banco['id'])
                pregunta_instance.texto = pregunta_banco['texto']
                pregunta_instance.tipo = pregunta_banco['tipo']
                # pregunta BANCO no tiene id
                opciones = pregunta_banco.pop('opciones', [])
                if pregunta_banco['tipo'] == 'O':
                    for opcion in pregunta_instance.opciones.all():
                        if not [el for el in opciones if ('id' in el) and (el['id'] == opcion.id)]:
                            opcion.delete()
                    for opcion in opciones:
                        if not 'id' in opcion:
                            PreguntaOpcion.objects.create(pregunta_banco=pregunta_instance, **opcion)
                        else:
                            opcion_instance = PreguntaOpcion.objects.get(
                                id=opcion['id'])
                            opcion_instance.texto = opcion['texto']
                            opcion_instance.correcta = opcion['correcta']
                            opcion_instance.save()
                else:
                    PreguntaOpcion.objects.filter(pregunta_banco=pregunta_instance).delete()
                pregunta_instance.save()
        return instance



# cuestonario pregunta
class CuestionarioPreguntaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    pregunta_banco = PreguntaBancoSerializer(required=True)

    class Meta:
        model = CuestionarioPregunta
        fields = [
            'id',
            'intentos_disponibles',
            'puntaje_asignado',
            'nombre',
            'pregunta_banco',
            'creation_date'
        ]
        extra_kwargs = {
            'id': {'required': False},
            'creation_date': {'read_only': True},
            'nombre': {'required': False},
        }

class CuestionarioSerializer(ModelSerializer):
    curso = SlugRelatedField(read_only=True, slug_field='nombre')
    cuestionario_banco = CuestionarioBancoSerializer(required=True)

    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'cuestionario_banco',
            'curso',
            'creation_date',
            'soluciones'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
            'soluciones': {'read_only': True},
        }

    def create(self, validated_data):
        data_cuestionario = validated_data.pop('cuestionario_banco')
        # cuestionario create
        if 'id' in data_cuestionario:
            cuestionario = CuestionarioBanco.objects.get(id=data_cuestionario['id'])
        else:
            preguntas = data_cuestionario.pop('preguntas', [])
            cuestionario = CuestionarioBanco.objects.create(**data_cuestionario)
            # pregunta del cuestionario
            for pregunta_banco in preguntas:
                if 'id' in pregunta_banco:
                    pregunta = PreguntaBanco.objects.get(id=pregunta_banco['id'])
                else:
                    opciones = pregunta_banco.pop('opciones', [])
                    pregunta = PreguntaBanco.objects.create(
                        **pregunta_banco, tipo_curso=cuestionario.tipo_curso)
                    if pregunta_banco['tipo'] == 'O':
                        for opcion in opciones:
                            PreguntaOpcion.objects.create(
                                pregunta=pregunta, **opcion)
                cuestionario.preguntas_banco.add(pregunta)
        return Cuestionario.objects.create(cuestionario_banco=cuestionario, **validated_data)

    def update(self, instance, validated_data):
        data_cuestionario = validated_data.pop('cuestionario_banco')
        instance.nombre =  validated_data.get('nombre', instance.nombre)
        # cuestionario create
        if instance.cuestionario_banco == data_cuestionario:
            cuestionario = CuestionarioBanco.objects.get(id=data_cuestionario['id'])
        else:
            preguntas = data_cuestionario.pop('preguntas', [])
            cuestionario = CuestionarioBanco.objects.create(**data_cuestionario)
            # pregunta del cuestionario
            for pregunta_banco in preguntas:
                if 'id' in pregunta_banco:
                    pregunta = PreguntaBanco.objects.get(id=pregunta_banco['id'])
                else:
                    opciones = pregunta_banco.pop('opciones', [])
                    pregunta = PreguntaBanco.objects.create(
                        **pregunta_banco, tipo_curso=cuestionario.tipo_curso)
                    if pregunta_banco['tipo'] == 'O':
                        for opcion in opciones:
                            PreguntaOpcion.objects.create(
                                pregunta=pregunta, **opcion)
                cuestionario.preguntas_banco.add(pregunta)
            instance.cuestionario_banco = cuestionario
        instance.save()
        return instance
        

class CuestionarioAlumnoSerializer(ModelSerializer):
    curso = SlugRelatedField(read_only=True, slug_field='nombre')
    class Meta:
        model = Cuestionario
        fields = [
            'id',
            'nombre',
            'fecha_asignacion',
            'fecha_expiracion',
            'curso',
            'creation_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creation_date': {'read_only': True},
        }

"""
Solucion de cuestionarios por parte del alumno
"""
class SolucionPreguntaSerializer(ModelSerializer):
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
    cuestionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Cuestionario.objects.all(), source='cuestionario')
    soluciones_preguntas = SolucionPreguntaSerializer(many=True)
    class Meta:
        model = Solucion
        fields = [
            'id',
            'comentario',
            'cuestionario_id',
            'soluciones_preguntas',
            'fecha_solucion',
            'fecha_revision'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'is_revisado': {'read_only': True},
            'comentario': {'required': False},
            'fecha_solucion': {'read_only': True},
            'fecha_revision': {'read_only': True},
        }
    
    def create(self, validated_data):
        soluciones = validated_data.pop('soluciones_preguntas', [])
        solucion = Solucion.objects.create(**validated_data)
        for opcion in soluciones:
            SolucionPregunta.objects.create(solucion=solucion, **opcion)
        return solucion


class SolucionDocenteSerializer(ModelSerializer):
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
            'id': {'read_only': True},
            'comentario': {'required': False},
            'fecha_solucion': {'read_only': True},
        }

    def update(self, instance, validated_data):
        soluciones = validated_data.pop('soluciones', [])
        instance.comentario = validated_data.get('comentario', instance.comentario)
        instance.fecha_revision = dt.now()
        instance.save()
        for pregunta in soluciones:
            if 'id' in pregunta:
                pregunta_instance = SolucionPregunta.objects.get(
                    id=pregunta['id'])
                pregunta_instance.puntaje_obtenido = pregunta['puntaje_obtenido']
                pregunta_instance.comentario = pregunta['comentario']
                pregunta_instance.situacion_respuesta = pregunta['situacion_respuesta']
                pregunta_instance.save()
        return instance