from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.institucion.models import Alumno, Docente
from apps.seguridad.models import User
from apps.seguridad.serializers import AlumnoSerializer, ChangePasswordSerializer, DocenteSerializer


class RegisterDocenteView(APIView):
    def post(self, request):
        data = {}
        try:
            user = User.objects.get(username=request.data.get('nro_documento', None))
            if user:
                data["msg"]="Ya existe el usuario"
                return Response(data,status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass
        serializer = DocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)


class RegisterAlumnoView(APIView):
    def post(self, request):
        serializer = AlumnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    def post(self, request):
        data = {}
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                data['msg'] = 'El usuario no existe.'
                return Response(data, status.HTTP_404_NOT_FOUND)

            valid_password = check_password(password, user.password)
            if not valid_password:
                data['msg'] = 'Contraseña incorrecta.'
                return Response(data, status.HTTP_401_UNAUTHORIZED)

            if user.is_valid_user():
                token, created = Token.objects.get_or_create(user=user)
                data['token'] = token.key
                data['created'] = created
                valid_user = False

                if user.is_admin_sistema():
                    data['tipo'] = 'admin'
                    valid_user = True

                elif user.is_docente() or user.is_admin_recursos():
                    docente = Docente.objects.filter(nro_documento=user.username).first()
                    if docente:
                        data['usuario'] = DocenteSerializer(docente).data
                        data['tipo'] = 'docente'
                        valid_user = True

                elif user.is_alumno():
                    alumno = Alumno.objects.filter(nro_documento=user.username).first()
                    if alumno:
                        data['usuario'] = AlumnoSerializer(alumno).data
                        data['tipo'] = 'alumno'
                        valid_user = True

                if valid_user:
                    return Response(data, status.HTTP_200_OK)

            data['msg'] = 'Usuario invalido.'
            return Response(data, status.HTTP_401_UNAUTHORIZED)
        data['msg'] = 'Credenciales invalidas.'
        return Response(data, status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data['msg'] = 'Se cerró la session'
        return Response(data, status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        data = {}
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                data = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'msg': 'Contraseña actualizada correctamente',
                }
                return Response(data, status.HTTP_200_OK)
            data['old_password'] = ['Contraseña incorrecta']
            return Response(data, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
