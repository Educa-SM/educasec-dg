from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response

class InstitucionesView(APIView):
    def get(self, request):
        instituciones = Institucion.objects.all()
        serializer = InstitucionSerializer(instituciones, many=True)
        return Response(serializer.data)



