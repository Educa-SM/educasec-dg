from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cuestionarios.serializers import *

# *********************** DOCENTE *****************************************
# --------------   Cuestionarios      -----------------------------------
class CuestionarioCursoView(APIView):
    permission_classes = [IsAuthenticated]
    # Cuestionarios de CursoId
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                page = request.query_params.get('page', 1)
                page_size = request.query_params.get('page_size', 1)
                search = request.query_params.get('search', '')
                cuestionarios = Cuestionario.objects.filter(
                    curso__id = id
                ).filter(
                    nombre__icontains = search
                ).order_by('id').reverse()
                paginator = Paginator(cuestionarios, page_size)
                serializer = CuestionarioListSerializer(paginator.get_page(page), many=True)
                return Response({
                    'data': serializer.data,
                    'numPages': paginator.num_pages,
                }, status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except Cuestionario.DoesNotExist or Curso.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)
        
class CuestionarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        if usuario.is_docente():
            serializer = CuestionarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

class CuestionarioDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # Cuestionarios de Curso con id
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                cuestionarios = Cuestionario.objects.get(id=id)
                serializer = CuestionarioSerializer(cuestionarios)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except Cuestionario.DoesNotExist or Curso.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)

    # Eliminar Cuestionario
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                cuestionario = Cuestionario.objects.get(id=id)
                cuestionario.delete()
                return Response({'msg': 'Eliminado'}, 200)
            except Cuestionario.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de Cuestionario
    def put(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                cuestionario = Cuestionario.objects.get(id=id)
                serializer = CuestionarioSerializer(cuestionario, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            except Cuestionario.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
        
class CuestionarioImagenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]    
    def patch(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                file_img = request.data.get('imagen')
                cuestionario = Cuestionario.objects.get(id=id)
                if cuestionario.imagen:
                    cuestionario.imagen.delete()
                cuestionario.imagen = file_img
                cuestionario.save()
                return Response({'msg': 'Actualizado'}, 200)
            except Pregunta.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
    # Eliminar Imagen Cuestionario
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                cuestionario = Cuestionario.objects.get(id=id)
                if cuestionario.imagen:
                    cuestionario.imagen.delete()
                cuestionario.save()
                return Response({'msg': 'Imagen Eliminada'}, 200)
            except Cuestionario.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

# *************************ALUMNO*************************************************
""" 
listar cueestionario de un alumno por su id de curso docente 
CUESTIONARIOS QUE AUN NO RESUELVE
"""
class ListCuestionarioAlumnoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del curso
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                inscripcion = AlumnoInscripcionCurso.objects.get(alumno__id=alumno.id,curso__id=id)
                if inscripcion.estate==EstadoCursoInscripcion.PENDIENTE:
                    return Response([], 200)
                # 2 states: EN_PROCESO, EN_REVISION
                cuestionarios = Cuestionario.objects.filter(curso__id=id).exclude(
                        soluciones__alumno=alumno, 
                        soluciones__estate=EstadoSolucion.EN_REVISION
                    ).exclude(soluciones__estate=EstadoSolucion.REVISADA).order_by('id').reverse()
                serializer = CuestionarioAlumnoSerializer(
                    cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)


"""
lISTA DE CUESTIONARIOS RESUELTOS POR EL ALUMNO
"""
class ListCuestionarioResueltosView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del curso docente --->

    def get(self, request, id):
        try:
            curso = Curso.objects.get(id=id)
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                inscripcion = AlumnoInscripcionCurso.objects.get(alumno__id=alumno.id,curso__id=id)
                if inscripcion.estate==EstadoCursoInscripcion.PENDIENTE:
                    return Response([], 200)
                cuestionarios = Cuestionario.objects.filter(curso=curso).filter(soluciones__alumno=alumno
                                    ).exclude(soluciones__estate=EstadoSolucion.EN_PROCESO).order_by('id').reverse()
                serializer = CuestionarioAlumnoSerializer(
                    cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist or Curso.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)


# cuestionarios de un alumno por su curso -> lista de preguntas
class CuestionarioAlumnoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del cuestionario

    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_alumno():
                cuestionarios = Cuestionario.objects.get(id=id)
                serializer = CuestionarioAlumnoSerializer(cuestionarios)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)
