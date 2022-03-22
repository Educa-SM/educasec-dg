from rest_framework.views import APIView

from apps.seguridad.serializers import UserSerializer
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class NivelesView(APIView):
   def get(self,request):
      niveles = Nivel.objects.all()
      serializer_levels = NivelSerializer(niveles, many=True)
      return Response(serializer_levels.data,201)

class CursoDocenteListView(APIView):
   permission_classes = [IsAuthenticated]
   def post(self,request):
      serializer = CursoDocenteSerializer(data=request.data)
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         docente = Docente.objects.get(nro_documento=user_ser.data['username'])
         if serializer.is_valid():
            serializer.save(docente=docente)
            return Response(serializer.data, 201)
         return Response(serializer.errors, 404)
      else:
         return Response({'msg':'No autorizado'},401)

class CursoDocenteView(APIView):
   # id dela institucion
   def get(self,request,id):
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         try:
            institucion =  Institucion.objects.get(id=id)
            docente = Docente.objects.get(nro_documento=user_ser.data['username'])
            cursos = CursoDocente.objects.filter(
                     docente=docente, 
                     institucion=institucion, 
                     estate='A')
            serializer = CursoDocenteSerializer(cursos, many=True)
            return Response(serializer.data,200)
         except CursoDocente.DoesNotExist or Docente.DoesNotExist or Institucion.DoesNotExist:
            return Response({'msg':'No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)
   
   def delete(self,request,id):
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         try:
            curso = CursoDocente.objects.get(id=id)
            docente = Docente.objects.get(nro_documento=user_ser.data['username'])
            if curso.docente==docente:
               curso.estate='I'
               curso.save()
               return Response(status = 204)
            else:
               return Response({'msg':'No le pertenece este curso'},401)
         except CursoDocente.DoesNotExist or Docente.DoesNotExist:
            return Response({'msg':'No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)
   
   def put(self,request,id):
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         try:
            curso = CursoDocente.objects.get(id=id)
            docente = Docente.objects.get(nro_documento=user_ser.data['username'])
            if curso.docente==docente:
               serializer= CursoDocenteSerializer(curso,data=request.data)
               if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, 200)
               return Response(serializer.errors, 404)
            else:
               return Response({'msg':'No le pertenece este curso'},401)
         except CursoDocente.DoesNotExist or Docente.DoesNotExist:
            return Response({'msg':'No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)

class CursoInscripcionView(APIView):
   def get(self, request):
      user_ser = UserSerializer(request.user)
      if 4  in user_ser.data['groups']:
         try:
            alumno = Alumno.objects.get(nro_documento=user_ser.data['username'])
            inscripciones = AlumnoInscripcionCurso.objects.filter(alumno = alumno)
            serializer = IncripcionCursoSerializer(inscripciones, many=True)
            return Response(serializer.data,200)
         except Alumno.DoesNotExist:
            return Response({'msg':'No Existe el curso'},404)
      else:
         return Response({'msg':'No autorizado'},401)

   def post(self, request):
      user_ser = UserSerializer(request.user)
      if 4  in user_ser.data['groups']:
         try:
            curso_docente = CursoDocente.objects.get(codigo_inscripcion=request.data['codigo'])
            alumno = Alumno.objects.get(nro_documento=user_ser.data['username'])
            if AlumnoInscripcionCurso.objects.filter(alumno = alumno,
                  curso_docente=curso_docente).exists():
               return Response({'msg':'Usted ya se a registrado a este curso'},400)
            else:
               inscripcion = AlumnoInscripcionCurso(alumno=alumno, curso_docente=curso_docente)
               inscripcion.save()
               return Response({'msg':'Creado'},201)
         except CursoDocente.DoesNotExist or Alumno.DoesNotExist:
            return Response({'msg':'No Existe el curso'},404)
      else:
         return Response({'msg':'No autorizado'},401)

   # actualizar el registro aceptar
   def put(self,request,id):
      user_ser = UserSerializer(request.user)
      if 2 in user_ser.data['groups']:
         try:
            curso = CursoDocente.objects.get(id=id)
            docente = Docente.objects.get(nro_documento=user_ser.data['username'])
            if curso.docente==docente:
               serializer= CursoDocenteSerializer(curso,data=request.data)
               if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, 200)
               return Response(serializer.errors, 404)
            else:
               return Response({'msg':'No le pertenece este curso'},401)
         except CursoDocente.DoesNotExist or Docente.DoesNotExist:
            return Response({'msg':'No Existe'},404)
      else:
         return Response({'msg':'No autorizado'},401)