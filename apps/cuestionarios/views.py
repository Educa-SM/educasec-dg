from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.seguridad.serializers import UserSerializer
# Create your views here.


class CuestionarioCursoView(APIView):
   permission_classes = [IsAuthenticated]
   # id del curso docente
   def get(self, request, id ):
      try:
         curso_docente = CursoDocente.objects.get(id=id)
         user_ser = UserSerializer(request.user)
         if 2 in user_ser.data['groups']:
            cuestionarios = CuestionarioCurso.objects.filter(curso_docente=curso_docente).order_by('id').reverse()
            serializer = CuestionarioCursoSerializer(cuestionarios, many=True)
            return Response(serializer.data, 200)
         else:
            return Response({'msg':'No autorizado'},401)
      except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist :
         return Response({'msg':'El cuestionario No Existe'},404)
   
   # id del Curso Docente
   def post(self, request,id):
      try:
         curso_docente = CursoDocente.objects.get(id=id)
         user_ser = UserSerializer(request.user)
         if 2 in user_ser.data['groups']:
            serializer = CuestionarioCursoSerializer(data=request.data)
            if serializer.is_valid():
               serializer.save(curso_docente=curso_docente)
               return Response(serializer.data, 201)
            return Response(serializer.errors, 404)
         else:
            return Response({'msg':'No autorizado'},401)
      except CursoDocente.DoesNotExist :
            return Response({'msg':'El curso No Existe'},404)

   # id del Cuestionario
   def delete(self, request, id):
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         try:
            cuestionario = CuestionarioCurso.objects.get(id=id)
            cuestionario.delete()
            return Response({'msg':'Eliminado'}, 200)
         except CuestionarioCurso.DoesNotExist :
            return Response({'msg':'El cuestionario No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)
   
   # id del Cuestionario
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
         except CuestionarioCurso.DoesNotExist :
            return Response({'msg':'El cuestionario No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)

class CuestionarioAlumnoView(APIView):
   permission_classes = [IsAuthenticated]
   # id del curso docente
   def get(self, request, id):
      try:
         curso_docente = CursoDocente.objects.get(id=id)
         user_ser = UserSerializer(request.user)
         if 4 in user_ser.data['groups']:
            cuestionarios = CuestionarioCurso.objects.filter(curso_docente=curso_docente).order_by('id').reverse()
            serializer = CuestionarioCursoSerializer(cuestionarios, many=True)
            return Response(serializer.data, 200)
         else:
            return Response({'msg':'No autorizado'},401)
      except CuestionarioCurso.DoesNotExist or CursoDocente.DoesNotExist :
         return Response({'msg':'El cuestionario No Existe'},404)