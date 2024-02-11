from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


############################# Recurso #############################
class RecursoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        estate = request.query_params.get('estate', None)
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 1)
        search = request.query_params.get('search', '')

        recursos = Recurso.objects.filter(titulo__icontains=search).order_by('-id')

        if estate:
            if estate == 'true':
                estate = 'A'
            elif estate == 'false':
                estate = 'I'
            recursos = recursos.filter(estate=estate)

        paginator = Paginator(recursos, page_size)
        serializer = RecursoSerializer2(paginator.get_page(page), many=True)
        data = {
            'data':serializer.data,
            'numPages':paginator.num_pages
        }
        return Response(data, status.HTTP_200_OK)

    # Creacion de Recurso
    def post(self, request):
        data = {}
        try:
            usuario = request.user
            if usuario.is_admin_recursos():
                serializer = RecursoSerializer2(data=request.data)
                if serializer.is_valid():
                    institucion_id = request.data.get('institucion', None)
                    institucion = Institucion.objects.filter(id=institucion_id).first()
                    if institucion:
                        serializer.save(institucion=institucion)
                    else:
                        serializer.save()
                    data = serializer.data
                    return Response(data, status.HTTP_201_CREATED)

                data = serializer.errors
                return Response(data, status.HTTP_400_BAD_REQUEST)
            else:
                data['msg'] = 'No Autorizado.'
                return Response(data, status.HTTP_401_UNAUTHORIZED)
        except:
            data['msg'] = 'Error inesperado.'
            return Response(data, status.HTTP_400_BAD_REQUEST)


class RecursoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, id):
        try:
            return Recurso.objects.get(id=id)
        except Recurso.DoesNotExist:
            raise Http404

    # Obtener Recurso con id
    def get(self, request, id, *args, **kwargs):
        data = {}
        object = self.get_object(id)
        serializer = RecursoSerializer(object, many=False)
        data = serializer.data
        return Response(data, status.HTTP_200_OK)

    # Modificar Recurso con id
    def put(self, request, id):
        data = {}
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                recurso = self.get_object(id)
                serializer = RecursoSerializer2(recurso, data=request.data)
                if serializer.is_valid():
                    if 'miniatura' in serializer.validated_data:
                        recurso.miniatura.delete()
                    if 'original_filename' in serializer.validated_data:
                        recurso.original_filename.delete()
                    serializer.save()
                    data = serializer.data
                    return Response(data, status.HTTP_200_OK)
                data = serializer.errors
                return Response(data, status.HTTP_400_BAD_REQUEST)
            except Recurso.DoesNotExist:
                data['msg'] = 'Recurso no encontrado.'
                return Response(data, status.HTTP_404_NOT_FOUND)
        else:
            data['msg'] = 'No autorizado.'
            return Response(data, status.HTTP_401_UNAUTHORIZED)

    # Eliminar Recurso con id
    def delete(self, request, id):
        data = {}
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                recurso = Recurso.objects.get(id=id)
                if recurso.miniatura:
                    recurso.miniatura.delete()
                if recurso.original_filename:
                    recurso.original_filename.delete()
                recurso.delete()
                data['msg'] = 'Recurso eliminado correctamente.'
                return Response(data, status.HTTP_200_OK)
            except Recurso.DoesNotExist:
                data['msg'] = 'Recurso no encontrado.'
                return Response(data, status.HTTP_404_NOT_FOUND)
        else:
            data['msg'] = 'Usuario no autorizado para realizar esta acción.'
            return Response(data, status.HTTP_401_UNAUTHORIZED)


class RecursoPublicAPIView(APIView):
    # Obtener Lista de Recursos
    def get(self, request):
        data = {}
        try:
            tipo = request.query_params.get('tipo', None)
            recurso = None
            if tipo:
                if not is_recurso_grupo(tipo):
                    data['msg'] = 'No exite el grupo de recursos'
                    return Response(data, status.HTTP_400_BAD_REQUEST)
                filters_tipos = get_grupo_recurso(tipo)
                recurso = Recurso.objects.filter(tipo__in=filters_tipos).order_by('id')
            else:
                recurso = Recurso.objects.all().order_by('id')
            serializer = RecursoSerializer(recurso, many=True)
            data = serializer.data
            return Response(data, status.HTTP_200_OK)
        except:
            data['msg'] = 'Error Inesperado.'
            return Response(data, status.HTTP_400_BAD_REQUEST)


class RecursoPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Recurso.objects.get(id=id)
        except Recurso.DoesNotExist:
            raise Http404

    # Obtener Recurso con id
    def get(self, request, id):
        data = {}
        try:
            recurso = self.get_object(id)
            serializer = RecursoSerializer2(recurso, many=False)
            data = serializer.data
            return Response(data, status.HTTP_200_OK)
        except Recurso.DoesNotExist:
            data['msg'] = 'Error inesperado.'
            return Response(data, status.HTTP_400_BAD_REQUEST)


############################# Patrocinador #############################
class PatrocinadorListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Creacion de Patrocinador
    def post(self, request):
        try:
            usuario = request.user
            if usuario.is_admin_recursos():
                serializer = PatrocinadorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except Exception  as msgError:
            return Response({'msg': 'Error inesperado.', 'data': str(msgError)}, status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data, status.HTTP_200_OK)

    # Modificar Patrocinador con id
    def put(self, request, id):
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                object = self.get_object(id)
                serializer = PatrocinadorSerializer(object, data=request.data)
                if serializer.is_valid():
                    if 'logo' in serializer.validated_data:
                        object.logo.delete()
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            except Patrocinador.DoesNotExist:
                return Response({'msg': 'Patrocinador no encontrado.'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado.'}, status.HTTP_401_UNAUTHORIZED)

    # Eliminar Patrocinador con id
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                object = self.get_object(id)
                if object.logo:
                    object.logo.delete()
                object.delete()
                return Response({'msg': 'Patrocinador eliminado correctamente.'}, status.HTTP_200_OK)
            except Patrocinador.DoesNotExist:
                return Response({'msg': 'Patrocinador no encontrado.'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción.'}, status.HTTP_401_UNAUTHORIZED)


class PatrocinadorPublicAPIView(APIView):
    # Obtener Lista de Patrocinadores
    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 1)
            search = request.query_params.get('search', '')

            patrocinadores = Patrocinador.objects.filter(nombre__icontains=search).order_by('-id')
            paginator = Paginator(patrocinadores, page_size)
            serializer = PatrocinadorSerializer(paginator.get_page(page), many=True)

            data = {
                'data': serializer.data,
                'numPages': paginator.num_pages
            }
            return Response(data, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Error Inesperado.'}, status.HTTP_400_BAD_REQUEST)


class PatrocinadorPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Patrocinador.objects.get(id=id)
        except Patrocinador.DoesNotExist:
            raise Http404

    # Obtener Patrocinador con id
    def get(self, request, id):
        try:
            object = self.get_object(id)
            serializer = PatrocinadorSerializer(object, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except Patrocinador.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)


############################# MiembroProyecto #############################
class MiembroProyectoListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Creacion de MiembroProyecto
    def post(self, request):
        try:
            usuario = request.user
            if usuario.is_admin_recursos():
                serializer = MiembroProyectoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.data, status.HTTP_200_OK)

    # Modificar MiembroProyecto con id
    def put(self, request, id):
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                object = self.get_object(id)
                serializer = MiembroProyectoSerializer(
                    object, data=request.data)
                if serializer.is_valid():
                    if 'logo' in serializer.validated_data:
                        object.logo.delete()
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            except MiembroProyecto.DoesNotExist:
                return Response({'msg': 'Miembro de Proyecto no encontrado.'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'No autorizado.'}, status.HTTP_401_UNAUTHORIZED)

    # Eliminar MiembroProyecto con id
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_admin_recursos():
            try:
                object = self.get_object(id)
                if object.logo:
                    object.logo.delete()
                object.delete()
                return Response({'msg': 'Miembro de Proyecto eliminado correctamente.'}, status.HTTP_200_OK)
            except MiembroProyecto.DoesNotExist:
                return Response({'msg': 'Miembro de Proyecto no encontrado.'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'Usuario no autorizado para realizar esta acción.'}, status.HTTP_401_UNAUTHORIZED)


class MiembroProyectoPublicAPIView(APIView):
    # Obtener Lista de Miembros de Proyecto
    def get(self, request):
        try:
            object = MiembroProyecto.objects.all().order_by('id').reverse()
            serializer = MiembroProyectoSerializer(object, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Error Inesperado.'}, status.HTTP_400_BAD_REQUEST)


class MiembroProyectoPublicDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return MiembroProyecto.objects.get(id=id)
        except MiembroProyecto.DoesNotExist:
            raise Http404

    # Obtener Miembro de Proyecto con id
    def get(self, request, id):
        try:
            object = self.get_object(id)
            serializer = MiembroProyectoSerializer(object, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except MiembroProyecto.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)
