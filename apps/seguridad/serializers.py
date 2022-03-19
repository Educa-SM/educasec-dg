from rest_framework import serializers
from apps.institucion.models import Alumno, Docente, Institucion
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

class InstitucionesSerializer(serializers.ModelSerializer):
   class Meta:
      model= Institucion
      fields = [
         'id',
         'nombre'
      ]      

class DocenteSerializer(serializers.ModelSerializer):
   user = UserSerializer()
   """instituciones = serializers.SlugRelatedField(
      many=True, read_only=True, slug_field='id'
   )"""
   instituciones = InstitucionesSerializer(many=True, read_only=True)
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
