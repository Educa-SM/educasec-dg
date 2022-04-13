from django.http import Http404
from rest_framework.views import APIView
from apps.seguridad.serializers import UserSerializer
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


class RecursoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None, *args, **kwargs):
        estate = request.query_params.get('estate', None)

        if estate:
            if estate == 'true':
                estate = 'A'
            elif estate == 'false':
                estate = 'I'

            recursos = Recurso.objects.filter(estate=estate).order_by('id').reverse()
        else:
            recursos = Recurso.objects.all().order_by('id').reverse()

        serializer = RecursoSerializer2(recursos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            user_ser = UserSerializer(request.user)
            if 3 in user_ser.data['groups']:
                serializer = RecursoSerializer2(data=request.data)
                institucion = Institucion.objects.get(
                    id=request.data['institucion'])
                if serializer.is_valid():
                    serializer.save(institucion=institucion)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'msg': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)
        except Recurso.DoesNotExist:
            return Response({'msg': 'El Recurso No Existe'}, status=status.HTTP_404_NOT_FOUND)


class RecursoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            return Recurso.objects.get(id=id)
        except Recurso.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None, *args, **kwargs):
        object = self.get_object(id)
        serializer = RecursoSerializer(object, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        user_ser = UserSerializer(request.user)
        if 3 in user_ser.data['groups']:
            try:
                recurso = self.get_object(id)
                serializer = RecursoSerializer(recurso, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Recurso.DoesNotExist:
                return Response({'msg': 'El Recurso No Existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id, format=None):
        user = UserSerializer(request.user)
        if 3 in user.data['groups']:
            try:
                recurso = Recurso.objects.get(id=id)
                if recurso.miniatura:
                    recurso.miniatura.delete()
                if recurso.original_filename:
                    recurso.original_filename.delete()
                recurso.delete()
                return Response({'msg': 'Recurso eliminado correctamente'}, status=status.HTTP_200_OK)
            except Recurso.DoesNotExist:
                return Response({'msg': 'El recurso no existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción'}, status=status.HTTP_401_UNAUTHORIZED)

class RecursoPublicView(APIView):
    def get(self, request, format=None):
        try:
            recurso = Recurso.objects.all().order_by('id').reverse()
            serializer = RecursoSerializer(recurso, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recurso.DoesNotExist:
            return Response({'msg': 'Los recurso no existe'}, status=status.HTTP_404_NOT_FOUND)
class RecursoPublicDetailView(APIView):
    def get(self, request,id, format=None):
        try:
            recurso = Recurso.objects.get(id=id)
            serializer = RecursoSerializer2(recurso, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recurso.DoesNotExist:
            return Response({'msg': 'Los recurso no existe'}, status=status.HTTP_404_NOT_FOUND)