from rest_framework.views import APIView
from apps.seguridad.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout, login
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


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


class LoginView(APIView):
   def post(self,request):
      username = request.data['username']
      password = request.data['password']
      try:
         user=User.objects.get(username=username)
      except User.DoesNotExist:
         return Response({'msg':'El usuario no existe'},404)
      pwd_Validate= check_password(password, user.password)
      if not pwd_Validate:
         return Response({'msg':'Contraseña incorrecta'}, 401)
      token, created = Token.objects.get_or_create(user=user)
      user_ser = UserSerializer(user)
      data  = {
         'token': token.key,
         'created': created,
      }
      if user_ser.data['groups'][0]==1:
         data['tipo']='admin'
      if user_ser.data['groups'][0]==2 or user_ser.data['groups'][0]==3:
         data['tipo']='docente'
         docente = Docente.objects.get(nro_documento=user.username)
         data['usuario']= DocenteSerializer(docente).data
         
      if user_ser.data['groups'][0]==4:
         data['tipo']='alumno'
         alumno = Alumno.objects.get(nro_documento=user.username)
         data['usuario']= AlumnoSerializer(alumno).data
         
      return Response(data,
         status=201)

class LogoutView(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
      try:
         request.user.auth_token.delete()
      except (AttributeError, ObjectDoesNotExist):
         pass
      logout(request)
      return Response({'msg':'Se cerró la session'},200)
