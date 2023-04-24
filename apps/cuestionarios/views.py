from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

# *********************** DOCENTE *****************************************
# --------------   Preguntas      -----------------------------------
class PreguntaCursoView(APIView):
    permission_classes = [IsAuthenticated]
     # id de Curso
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                preguntas = Pregunta.objects.filter(cuestionario__curso__id=id).order_by('id').reverse()
                serializer = PreguntaSerializer(preguntas, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Pregunta.DoesNotExist or Curso.DoesNotExist:
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
            tipo_curso = TipoCurso.objects.get(id=id)
            usuario = request.user
            if usuario.is_docente():
                preguntas = Pregunta.objects.filter(
                    cuestionario__curso__tipo_curso=tipo_curso).order_by('id').reverse()
                serializer = PreguntaSerializer(preguntas, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except TipoCurso.DoesNotExist or Pregunta.DoesNotExist:
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
        

# --------------   Cuestionarios      -----------------------------------
class CuestionarioCursoView(APIView):
    permission_classes = [IsAuthenticated]
    # Cuestionarios de CursoId
    def get(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                cuestionarios = Cuestionario.objects.filter(curso__id = id).order_by('id').reverse()
                serializer = CuestionarioListSerializer(cuestionarios, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
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
        except Solucion.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)
    
    # metodo del docente -> id de la solucin
    def delete(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                try:
                    solucion = Solucion.objects.get(id=id)
                    solucion.delete()
                    return Response({'msg': 'Eliminado'}, 200)
                except Solucion.DoesNotExist:
                    return Response({'msg': 'El cuestionario No Existe'}, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Solucion.DoesNotExist:
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
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                inscripcion = AlumnoInscripcionCurso.objects.get(alumno__id=alumno.id,curso__id=id)
                if inscripcion.estate=='A':
                    return Response([], 200)
                cuestionarios = Cuestionario.objects.filter(
                    curso__id=id).exclude(soluciones__alumno=alumno).order_by('id').reverse()
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
                if inscripcion.estate=='A':
                    return Response([], 200)
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
