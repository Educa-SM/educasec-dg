from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.seguridad.serializers import UserSerializer
from .serializers import *


############################# Recurso #############################
class RecursoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # ???????????????
    def get(self, request, format=None, *args, **kwargs):
        estate = request.query_params.get('estate', None)
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 1)
        if estate:
            if estate == 'true':
                estate = 'A'
            elif estate == 'false':
                estate = 'I'

            recursos = Recurso.objects.filter(
                estate=estate).order_by('id').reverse()
        else:
            recursos = Recurso.objects.all().order_by('id').reverse()
        paginator = Paginator(recursos, page_size)
        serializer = RecursoSerializer2(
            paginator.get_page(page_number), many=True)
        data = {
            'data': serializer.data,
            'numPages': paginator.num_pages,
        }
        return Response(data, status.HTTP_200_OK)

    # Creacion de Recurso
    def post(self, request, format=None):
        try:
            user_ser = UserSerializer(request.user)
            if 3 in user_ser.data['groups']:
                serializer = RecursoSerializer2(data=request.data)
                if serializer.is_valid():
                    institucion = None
                    institucion_id = request.data.get('institucion', None)
                    try:
                        institucion = Institucion.objects.get(
                            id=institucion_id)
                    except:
                        pass
                    if institucion:
                        serializer.save(institucion=institucion)
                    else:
                        serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'No Autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class RecursoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            return Recurso.objects.get(id=id)
        except Recurso.DoesNotExist:
            raise Http404

    # Obtener Recurso con id
    def get(self, request, id, format=None, *args, **kwargs):
        object = self.get_object(id)
        serializer = RecursoSerializer(object, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Modificar Recurso con id
    def put(self, request, id, format=None):
        user_ser = UserSerializer(request.user)
        if 3 in user_ser.data['groups']:
            try:
                recurso = self.get_object(id)
                serializer = RecursoSerializer2(recurso, data=request.data)
                if serializer.is_valid():
                    if 'miniatura' in serializer.validated_data:
                        recurso.miniatura.delete()
                    if 'original_filename' in serializer.validated_data:
                        recurso.original_filename.delete()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Recurso.DoesNotExist:
                return Response({'msg': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Eliminar Recurso con id
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
                return Response({'msg': 'Recurso eliminado correctamente.'}, status=status.HTTP_200_OK)
            except Recurso.DoesNotExist:
                return Response({'msg': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción.'}, status=status.HTTP_401_UNAUTHORIZED)


class RecursoPublicAPIView(APIView):
    # Obtener Lista de Recursos
    def get(self, request, format=None):
        try:
            recurso = Recurso.objects.all().order_by('id').reverse()
            serializer = RecursoSerializer(recurso, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Error Inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class RecursoPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Recurso.objects.get(id=id)
        except Recurso.DoesNotExist:
            raise Http404

    # Obtener Recurso con id
    def get(self, request, id, format=None):
        try:
            recurso = self.get_object(id)
            serializer = RecursoSerializer2(recurso, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recurso.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


############################# Patrocinador #############################
class PatrocinadorListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Creacion de Patrocinador
    def post(self, request, format=None):
        try:
            user_ser = UserSerializer(request.user)
            if 3 in user_ser.data['groups']:
                serializer = PatrocinadorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'No Autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class PatrocinadorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            return Patrocinador.objects.get(id=id)
        except Patrocinador.DoesNotExist:
            raise Http404

    # Obtener Patrocinador con id
    def get(self, request, id, format=None, *args, **kwargs):
        object = self.get_object(id)
        serializer = PatrocinadorSerializer(object, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Modificar Patrocinador con id
    def put(self, request, id, format=None):
        user_ser = UserSerializer(request.user)
        if 3 in user_ser.data['groups']:
            try:
                object = self.get_object(id)
                serializer = PatrocinadorSerializer(object, data=request.data)
                if serializer.is_valid():
                    if 'logo' in serializer.validated_data:
                        object.logo.delete()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Patrocinador.DoesNotExist:
                return Response({'msg': 'Patrocinador no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Eliminar Patrocinador con id
    def delete(self, request, id, format=None):
        user = UserSerializer(request.user)
        if 3 in user.data['groups']:
            try:
                object = self.get_object(id)
                if object.logo:
                    object.logo.delete()
                object.delete()
                return Response({'msg': 'Patrocinador eliminado correctamente.'}, status=status.HTTP_200_OK)
            except Patrocinador.DoesNotExist:
                return Response({'msg': 'Patrocinador no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción.'}, status=status.HTTP_401_UNAUTHORIZED)


class PatrocinadorPublicAPIView(APIView):
    # Obtener Lista de Patrocinadores
    def get(self, request, format=None):
        try:
            object = Patrocinador.objects.all().order_by('id').reverse()
            serializer = PatrocinadorSerializer(object, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Error Inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class PatrocinadorPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Patrocinador.objects.get(id=id)
        except Patrocinador.DoesNotExist:
            raise Http404

    # Obtener Patrocinador con id
    def get(self, request, id, format=None):
        try:
            object = self.get_object(id)
            serializer = PatrocinadorSerializer(object, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patrocinador.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


############################# MiembroProyecto #############################
class MiembroProyectoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Creacion de MiembroProyecto
    def post(self, request, format=None):
        try:
            user_ser = UserSerializer(request.user)
            if 3 in user_ser.data['groups']:
                serializer = MiembroProyectoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'No Autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class MiembroProyectoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            return MiembroProyecto.objects.get(id=id)
        except MiembroProyecto.DoesNotExist:
            raise Http404

    # Obtener MiembroProyecto con id
    def get(self, request, id, format=None, *args, **kwargs):
        object = self.get_object(id)
        serializer = MiembroProyectoSerializer(object, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Modificar MiembroProyecto con id
    def put(self, request, id, format=None):
        user_ser = UserSerializer(request.user)
        if 3 in user_ser.data['groups']:
            try:
                object = self.get_object(id)
                serializer = MiembroProyectoSerializer(
                    object, data=request.data)
                if serializer.is_valid():
                    if 'logo' in serializer.validated_data:
                        object.logo.delete()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except MiembroProyecto.DoesNotExist:
                return Response({'msg': 'Miembro de Proyecto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Eliminar MiembroProyecto con id
    def delete(self, request, id, format=None):
        user = UserSerializer(request.user)
        if 3 in user.data['groups']:
            try:
                object = self.get_object(id)
                if object.logo:
                    object.logo.delete()
                object.delete()
                return Response({'msg': 'Miembro de Proyecto eliminado correctamente.'}, status=status.HTTP_200_OK)
            except MiembroProyecto.DoesNotExist:
                return Response({'msg': 'Miembro de Proyecto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción.'}, status=status.HTTP_401_UNAUTHORIZED)


class MiembroProyectoPublicAPIView(APIView):
    # Obtener Lista de Miembros de Proyecto
    def get(self, request, format=None):
        try:
            object = MiembroProyecto.objects.all().order_by('id').reverse()
            serializer = MiembroProyectoSerializer(object, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Error Inesperado.'}, status=status.HTTP_400_BAD_REQUEST)


class MiembroProyectoPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return MiembroProyecto.objects.get(id=id)
        except MiembroProyecto.DoesNotExist:
            raise Http404

    # Obtener Miembro de Proyecto con id
    def get(self, request, id, format=None):
        try:
            object = self.get_object(id)
            serializer = MiembroProyectoSerializer(object, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MiembroProyecto.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status=status.HTTP_400_BAD_REQUEST)
