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

class CursoDocenteView(APIView):
   permission_classes = [IsAuthenticated]
   def post(self,request):
      serializer = CursoDocenteSerializer(data=request.data)
      user_ser = UserSerializer(request.user)
      if user_ser.data['groups'][0]==2:
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
         return Response(serializer.errors, 404)
      else:
         return Response({'msg':'No autorizado'})
   
   def get(self,request):
      user_ser = UserSerializer(request.user)
      if user_ser.data['groups'][0]==2:
         docente = Docente.objects.get(nro_documento=user_ser.data['username'])
         cursos = CursoDocente.objects.filter(docente=docente)
         serializer = CursoDocenteSerializer(cursos, many=True)
         return Response(serializer.data,200)
      else:
         return Response({'msg':'No autorizado'})
