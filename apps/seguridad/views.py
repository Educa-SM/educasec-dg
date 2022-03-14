from rest_framework.views import APIView
from apps.seguridad.serializers import AlumnoSerializer, DocenteSerializer
from rest_framework.response import Response

class RegisterDocenteView(APIView):
   def post(self, request):
      serializer = DocenteSerializer(data = request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, 201)
      return Response(serializer.errors, 404)

class RegisterAlumnoView(APIView):
   def post(self, request):
      serializer = AlumnoSerializer(data = request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, 201)
      return Response(serializer.errors, 404)
