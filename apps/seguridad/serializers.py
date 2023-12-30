from rest_framework.serializers import CharField, ModelSerializer, PrimaryKeyRelatedField, Serializer, SlugRelatedField, IntegerField
from apps.institucion.models import Alumno, Docente, Institucion
from .models import User


class UserSerializer(ModelSerializer):
    groups = SlugRelatedField(
        many=True, read_only=True, slug_field='id'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'groups',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }


class InstitucionesSerializer(ModelSerializer):
    class Meta:
        model = Institucion
        fields = [
            'id',
            'nombre'
        ]


class DocenteSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    instituciones = InstitucionesSerializer(many=True, read_only=True)
    instituciones_id = PrimaryKeyRelatedField(
        queryset=Institucion.objects.all(), source='instituciones', required=False,
        write_only=True, many=True
    )

    class Meta:
        model = Docente
        fields = [
            'user',
            'nombres',
            'apellido_materno',
            'apellido_paterno',
            'direccion',
            'tipo_documento',
            'nro_documento',
            'instituciones',
            'instituciones_id',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'instituciones': {'read_only': True},
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        #data_user = validated_data.pop('user')
        user = User(username=validated_data['nro_documento'])
        user.set_password(validated_data['nro_documento'])
        user.save()
        user.groups.add(2)
        instituciones = validated_data.pop('instituciones')
        docente = Docente(**validated_data, user=user)
        docente.estate = 'P'
        docente.save()
        if not docente.id:
            user.delete()
        else:
            for inst in instituciones:
                docente.instituciones.add(inst)
        return docente

class AlumnoSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Alumno
        fields = [
            'id',
            'user',
            'nombres',
            'apellido_materno',
            'apellido_paterno',
            'tipo_documento',
            'nro_documento',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        data_user = validated_data.pop('user')
        user = User(**data_user)
        user.set_password(data_user['password'])
        user.save()
        user.groups.add(4)
        alumno = Alumno(**validated_data, user=user)
        alumno.save()
        if not alumno.id:
            user.delete()
        return alumno


class ChangePasswordSerializer(Serializer):
    model = User
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class PostRegistrarAlumnoCurso(Serializer):
    username = CharField(required=True, max_length=12)
    apellido_paterno = CharField(required=True, max_length=150)
    apellido_materno = CharField(required=True, max_length=150)
    tipo_documento = CharField(required=True,)
    id_curso = IntegerField(required=True)
