from rest_framework import serializers
from .models import *


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = [
            'titulo',
            'descripcion',
            'contenido',
            'tipo',
        ]

    def to_representation(self, instance):
        return instance.to_dict()


class RecursoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = [
            'titulo',
            'descripcion',
            'contenido',
            'tipo',
            'miniatura',
            'original_filename',
        ]

    def to_representation(self, instance):
        return instance.to_dict()
