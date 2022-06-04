from rest_framework import serializers
from .models import *


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = [
            'id',
            'titulo',
            'descripcion',
            'contenido',
            'tipo',
            'miniatura'
        ]


class RecursoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = [
            'id',
            'titulo',
            'descripcion',
            'contenido',
            'tipo',
            'miniatura',
            'original_filename',
            'creation_date',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'original_filename': {'required': False},
            'miniatura': {'required': False},
            'contenido': {'required': False},
            'creation_date': {'read_only': True},
        }


class PatrocinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrocinador
        fields = [
            'id',
            'nombre',
            'descripcion',
            'logo',
        ]


class MiembroProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiembroProyecto
        fields = '__all__'
