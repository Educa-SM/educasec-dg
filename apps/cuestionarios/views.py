from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


# --------------   Preguntas      -----------------------------------
class PreguntaBancoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            tipo_curso = TipoCurso.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                preguntas = PreguntaBanco.objects.filter(
                    tipo_curso=tipo_curso).order_by('id').reverse()
                serializer = PreguntaBancoSerializer(preguntas, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except TipoCurso.DoesNotExist or PreguntaBanco.DoesNotExist:
            return Response({'msg': 'No Existe'}, 404)

    def post(self, request, id):
        try:
            tipo_curso = TipoCurso.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                serializer = PreguntaBancoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(tipo_curso=tipo_curso)
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except TipoCurso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # id de la pregunta
    def put(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                pregunta = PreguntaBanco.objects.get(id=id)
                serializer = PreguntaBancoSerializer(pregunta, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            except PreguntaBanco.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de la pregunta
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                pregunta = PreguntaBanco.objects.get(id=id)
                pregunta.delete()
                return Response({'msg': 'Eliminado'}, 200)
            except PreguntaBanco.DoesNotExist:
                return Response({'msg': 'La pregunta No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


# --------------   Cuestionarios      -----------------------------------
class CuestionarioBancoView(APIView):
    permission_classes = [IsAuthenticated]
    # id del TipoCurso

    def post(self, request, id):
        try:
            tipo_curso = TipoCurso.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                serializer = CuestionarioBancoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(tipo_curso=tipo_curso)
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except TipoCurso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # id del tipo_curso
    def get(self, request, id):
        try:
            tipo_curso = TipoCurso.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                cuestionarios = CuestionarioBanco.objects.filter(
                    tipo_curso=tipo_curso).order_by('id').reverse()
                serializer = CuestionarioBancoSerializer(cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist or TipoCurso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # id del Cuestionario
    def delete(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                cuestionario = CuestionarioBanco.objects.get(id=id)
                cuestionario.delete()
                return Response({'msg': 'Eliminado'}, 200)
            except CuestionarioBanco.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id del Cuestionario
    def put(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                cuestionario = CuestionarioBanco.objects.get(id=id)
                serializer = CuestionarioBancoSerializer(
                    cuestionario, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            except CuestionarioBanco.DoesNotExist:
                return Response({'msg': 'El cuestionario No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


# *********************** DOCENTE *****************************************
class CuestionarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # id de Curso
    def get_object(self, id):
        try:
            return Curso.objects.get(id=id)
        except Curso.DoesNotExist:
            raise Http404

    # Cuestionarios de Curso con id
    def get(self, request, id):
        try:
            object = self.get_object(id)
            usuario = request.user
            if usuario.is_docente():
                cuestionarios = Cuestionario.objects.filter(curso=object).order_by('id')
                serializer = CuestionarioSerializer(cuestionarios, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        except Cuestionario.DoesNotExist or Curso.DoesNotExist:
            return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)

    # id del Curso  ????????????????????????????????
    def post(self, request, id):
        try:
            object = self.get_object(id)
            usuario = request.user
            if usuario.is_docente():
                serializer = CuestionarioSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(curso=object)
                    return Response(serializer.data, 201)
                return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Curso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

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


"""
Soluciones de cueestionario 
"""
class SolucionCuestionarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # ****   id = del cuestionario   ** * ***
    def get(self, request, id):
        try:
            usuario = request.user
            # alumno
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                solucion = Solucion.objects.filter(alumno=alumno, cuestionario__id=id).first()
                serializer = SolucionSerializer(solucion)
                return Response(serializer.data, 200)
            # docente
            elif usuario.is_docente():
                data = Solucion.objects.filter(cuestionario__id=id).order_by('id').reverse()
                serializer = SolucionDocenteSerializer(data, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Solucion.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # metodo del docente -> id de la solucin
    def put(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                solucion = Solucion.objects.get(id=id)
                serializer = SolucionDocenteSerializer(solucion, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Curso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)


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
            curso = Curso.objects.get(id=id)
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                cuestionarios = Cuestionario.objects.filter(
                    curso=curso).exclude(soluciones__alumno=alumno).order_by('id').reverse()
                serializer = CuestionarioAlumnoSerializer(
                    cuestionarios, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist or Curso.DoesNotExist:
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
                cuestionarios = Cuestionario.objects.filter(
                    curso=curso).filter(soluciones__alumno=alumno).order_by('id').reverse()
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
                serializer = CuestionarioSerializer(cuestionarios)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Cuestionario.DoesNotExist:
            return Response({'msg': 'El cuestionario No Existe'}, 404)


"""
Solucion de cuestionarios por parte del alumno
"""
class SolucionCursoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                solucion = Solucion.objects.filter(alumno=alumno, cuestionario__id=request.data['cuestionario_id'])
                if solucion:
                    return Response({'msg': 'Solucion ya registrada'}, 400)
                else:
                    serializer = SolucionSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(alumno=alumno)
                        return Response(serializer.data, 201)
                    return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Curso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)
