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

    """def to_representation(self, instance):
        return instance.to_dict()"""


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

    #def to_representation(self, instance):
    #    return instance.to_dict()
