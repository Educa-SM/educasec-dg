from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.seguridad.serializers import UserSerializer
from django.db.models import Q
from .serializers import *


class CuestionarioCursoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # id de CursoDocente
    def get_object(self, id):
        try:
            return CursoDocente.objects.get(id=id)
        except CursoDocente.DoesNotExist:
            raise Http404

    # Cuestionarios de CursoDocente
    def get(self, request, id):
        try:
            object = self.get_object(id)
            user_ser = UserSerializer(request.user)

            if 2 in user_ser.data['groups']:
                cuestionarios = CuestionarioCurso.objects.filter(curso_docente=object).order_by('-id')
                serializer = CuestionarioCursoSerializer(cuestionarios, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)

    # id del Curso Docente  ????????????????????????????????
    def post(self, request, id):
        try:
            object = self.get_object(id)
            user_ser = UserSerializer(request.user)
            if 2 in user_ser.data['groups']:
                serializer = CuestionarioCursoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(curso_docente=object)
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CursoDocente.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # Eliminar CuestionarioCurso
    def delete(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                cuestionario = CuestionarioCurso.objects.get(id=id)
                cuestionario.delete()
                return Response({'msg': 'Eliminado'}, 200)
            except CuestionarioCurso.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de Cuestionario
    def put(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                cuestionario_curso = CuestionarioCurso.objects.get(id=id)
                serializer = CuestionarioCursoSerializer(cuestionario_curso, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            except CuestionarioCurso.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


# cuestionarios de un alumno por su cursodocente -> lista de preguntas
class CuestionarioAlumnoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del cuestionario
    # ** alumno ***
    def get(self, request, id):
        try:
            user_ser = UserSerializer(request.user)
            if 4 in user_ser.data['groups']:
                cuestionarios = CuestionarioCurso.objects.get(id=id)
                serializer = CuestionarioCursoSerializer(cuestionarios)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)


""" 
listar cueestionario de un alumno por su id de curso docente 
CUESTIONARIOS QUE AUN NO RESUELVE
"""
class ListCuestionarioAlumnoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del curso docente --->
    # *** Alumno ***
    def get(self, request, id):
        try:
            curso_docente = CursoDocente.objects.get(id=id)
            user_ser = UserSerializer(request.user)
            if 4 in user_ser.data['groups']:
                alumno = Alumno.objects.get(user=request.user)
                cuestionarios = CuestionarioCurso.objects.filter(
                    curso_docente=curso_docente).exclude(soluciones__alumno=alumno).order_by('id').reverse()
                serializer = CuestionarioCursoAlumnoSerializer(
                    cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)
"""
lISTA DE CUESTIONARIOS RESUELTOS POR EL ALUMNO
"""
class ListCuestionarioResueltosView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # id del curso docente --->
    # *** Alumno ***
    def get(self, request, id):
        try:
            curso_docente = CursoDocente.objects.get(id=id)
            user_ser = UserSerializer(request.user)
            if 4 in user_ser.data['groups']:
                alumno = Alumno.objects.get(user=request.user)
                cuestionarios = CuestionarioCurso.objects.filter(
                    curso_docente=curso_docente).filter(soluciones__alumno=alumno).order_by('id').reverse()
                serializer = CuestionarioCursoAlumnoSerializer(
                    cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)


"""
Evaluar las soluciones de los alumnos -> Docente
"""
class EvaluarCuestionarioCursoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # metodo del docente
    def post(self, request, id):
        try:
            user_ser = UserSerializer(request.user)
            if 2 in user_ser.data['groups']:
                print(request.data)
                return Response({'msg': 'Ok'}, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CursoDocente.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)


"""
Solucion de cuestionarios por parte del alumno
"""
class SolucionCuestionarioCursoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #****   aLUMNO   ** * ***
    def post(self, request):
        try:
            user_ser = UserSerializer(request.user)
            if 4 in user_ser.data['groups']:
                alumno = Alumno.objects.get(user=request.user)
                serializer = SolucionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(alumno=alumno)
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CursoDocente.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

"""
Soluciones de cueestionario pasa -> cuestionario_curso_id
"""
class SolucionCuestionarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    #****   id = del cuestionario curso  ** * ***
    def get(self, request,id):
        try:
            user_ser = UserSerializer(request.user)
            # alumno
            if 4 in user_ser.data['groups']:
                alumno = Alumno.objects.get(user=request.user)
                solucion = SolucionCuestionario.objects.filter(alumno=alumno,cuestionario_curso__id=id).first()
                serializer = SolucionSerializer(solucion)
                return Response(serializer.data, 200)
            # docente
            if 2 in user_ser.data['groups']:
                data = SolucionCuestionario.objects.filter(cuestionario_curso__id=id).order_by('id').reverse()
                serializer = SolucionSerializer(data, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except CursoDocente.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

