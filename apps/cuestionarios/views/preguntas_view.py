from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cuestionarios.serializers import *

# *********************** DOCENTE *****************************************
# --------------   Preguntas      -----------------------------------
class PreguntaCursoView(APIView):
    permission_classes = [IsAuthenticated]
     # id de Curso
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                page = request.query_params.get('page', 1)
                page_size = request.query_params.get('page_size', 1)
                search = request.query_params.get('search', '')
                preguntas = Pregunta.objects.filter(
                    cuestionario__curso__id=id
                ).filter(texto__icontains=search).order_by('-id')
                paginator = Paginator(preguntas, page_size)
                serializer = PreguntaSerializer(paginator.get_page(page), many=True)
                return Response({
                    'data': serializer.data,
                    'numPages': paginator.num_pages,
                }, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Pregunta.DoesNotExist:
            return Response({'msg': 'No Existe'}, 404)
        
class PreguntaView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            usuario = request.user
            if usuario.is_docente():
                preguntas = Pregunta.objects.order_by('id').reverse()
                serializer = PreguntaSerializer(preguntas, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Pregunta.DoesNotExist:
            return Response({'msg': 'No Existe'}, 404)

    def post(self, request):
        try:
            usuario = request.user
            if usuario.is_docente():
                serializer = PreguntaSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Pregunta.DoesNotExist:
            return Response({'msg': 'Error'}, 404)

class PreguntaDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            grado = Grado.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                page = request.query_params.get('page', 1)
                page_size = request.query_params.get('page_size', 1)
                search = request.query_params.get('search', '')

                preguntas = Pregunta.objects.filter(
                        cuestionario__curso__grado=grado
                    ).filter(texto__icontains=search).order_by('id').reverse()
                paginator = Paginator(preguntas, page_size)
                serializer = PreguntaSerializer(paginator.get_page(page), many=True)
                return Response({
                    'data': serializer.data,
                    'numPages': paginator.num_pages,
                }, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Grado.DoesNotExist or Pregunta.DoesNotExist:
            return Response({'msg': 'No Existe'}, 404)
     # id de la pregunta
    def put(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                pregunta = Pregunta.objects.get(id=id)
                serializer = PreguntaSerializer(pregunta, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            except Pregunta.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de la pregunta
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                pregunta = Pregunta.objects.get(id=id)
                pregunta.delete()
                return Response({'msg': 'Eliminado'}, 200)
            except Pregunta.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
        

class PreguntaImagenView(APIView): 
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                file_img = request.data.get('imagen')
                pregunta = Pregunta.objects.get(id=id)
                if pregunta.imagen:
                    pregunta.imagen.delete()
                pregunta.imagen = file_img
                pregunta.save()
                return Response({'msg': 'Actualizado'}, 200)
            except Pregunta.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
    
    # Eliminar Imagen Pregunta
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                pregunta = Pregunta.objects.get(id=id)
                if pregunta.imagen:
                    pregunta.imagen.delete()
                pregunta.save()
                return Response({'msg': 'Imagen Eliminada'}, 200)
            except Cuestionario.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
     