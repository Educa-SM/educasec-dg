from rest_framework import serializers
from .models import Institucion, MensajeInicio


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = [
            'id',
            'nombre'
        ]

class MensajeInicioSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(max_length=255, allow_blank=True)
    feha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    imagen = serializers.ImageField()
    user = serializers.IntegerField()

    class Meta:
        model = MensajeInicio
        fields = [
            'titulo',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'imagen',
            'user',
        ]
        extra_kwargs = {
            'descripcion': {'required': False},
        }
