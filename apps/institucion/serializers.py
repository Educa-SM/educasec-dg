from rest_framework import serializers
from .models import Institucion, MensajeInicio
from apps.seguridad.models import User

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = [
            'id',
            'nombre'
        ]

class MensajeInicioPublicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeInicio
        fields = [
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'imagen'
        ]

class MensajeInicioSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='usuario', required=False)
    class Meta:
        model = MensajeInicio
        fields = [
            'id',
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'imagen',
            'user_id'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'descripcion': {'required': False},
            'user_id': {'read_only': True},
            'imagen': {'required': False}
        }
