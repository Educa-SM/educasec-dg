from rest_framework import serializers
from apps.alumno.models import Alumno
from apps.institucion.models import Docente
from .models import User

class UserSerializer(serializers.ModelSerializer):
   groups = serializers.SlugRelatedField(
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
      

class DocenteSerializer(serializers.ModelSerializer):
   user = UserSerializer()
   instituciones = serializers.SlugRelatedField(
      many=True, read_only=True, slug_field='id'
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
         'instituciones'
      ]
      extra_kwargs = {'id': 
         {'read_only': True},
         'instituciones': 
         {'read_only': True}
      }
   
   def create(self, validated_data):
      data_user = validated_data.pop('user')
      user = User(**data_user)
      user.set_password(data_user['password'])
      user.save()
      user.groups.add(2)
      docente = Docente(**validated_data,user=user)
      docente.save()
      if not docente.id:
         user.delete()
      return docente

class AlumnoSerializer(serializers.ModelSerializer):
   user = UserSerializer()

   class Meta:
      model = Alumno
      fields = [
         'user',
         'nombres',
         'apellido_materno',
         'apellido_paterno',
         'tipo_documento',
         'nro_documento'
      ]
      extra_kwargs = {'id': 
         {'read_only': True}
      }
   
   def create(self, validated_data):
      data_user = validated_data.pop('user')
      user = User(**data_user)
      user.set_password(data_user['password'])
      user.save()
      user.groups.add(4)
      alumno = Alumno(**validated_data,user=user)
      alumno.save()
      if not alumno.id:
         user.delete()
      return alumno
