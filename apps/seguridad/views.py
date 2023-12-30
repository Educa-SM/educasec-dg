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
from apps.seguridad.serializers import AlumnoSerializer, ChangePasswordSerializer, DocenteSerializer, PostRegistrarAlumnoCurso
from rest_framework.decorators import api_view, permission_classes
from apps.cursos.models import Curso, AlumnoInscripcionCurso, EstadoCursoInscripcion

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
                valid_user = False

                if user.is_admin_sistema():
                    data['tipo'] = 'admin'
                    valid_user = True

                elif user.is_docente() or user.is_admin_recursos():
                    docente = Docente.objects.filter(nro_documento=user.username).first()
                    if docente:
                        if docente.estate == 'P':
                            data['msg'] = 'Usuario pendiente de aprobación.'
                            return Response(data, status.HTTP_401_UNAUTHORIZED)
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
                    token, created = Token.objects.get_or_create(user=user)
                    data['token'] = token.key
                    data['created'] = created
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


# --- aceptar docente con permission_classes IsAuthenticated
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def aceptar_docente(request):
    respuesta = {}
    datos = request.data
    docente_id = datos['docente_id']
    estate = datos['estate']
    try:
        docente = Docente.objects.get(id=docente_id)
    except Docente.DoesNotExist:
        respuesta['msg'] = 'El docente no existe'
        return Response(respuesta, status.HTTP_404_NOT_FOUND)
    
    if docente.estate == estate:
        respuesta['msg'] = 'El docente tiene el mismo estado'
        return Response(respuesta, status.HTTP_400_BAD_REQUEST)
    
    docente.estate = estate
    docente.save()
    respuesta = {
        'docente_id': docente_id,
        'estado': docente.estate,
        'msg': 'El estado fue actualizado correctamente',
        'status': 'success',
    }
    return Response(respuesta, status.HTTP_200_OK)

#--- bucar estudiante por nro_documento
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_estudiante_by_nro_documento(request, nro_documento):
    try:
        usuario = request.user
        if not usuario.is_docente():
            return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        user_found = User.objects.filter(username=nro_documento).first()
        if not user_found:
            return Response({'msg': 'El usuario no existe.'}, status.HTTP_404_NOT_FOUND)
        if user_found.is_alumno():
            estudiante = Alumno.objects.filter(nro_documento=nro_documento).first()
            if not estudiante:
                return Response({'msg': 'El estudiante no existe.'}, status.HTTP_404_NOT_FOUND)
            serializer = AlumnoSerializer(estudiante)
            return Response(serializer.data)
        else:
            return Response({'msg': 'El usuario no es estudiante.'}, status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)

# registrar alumno y agregarlo al curso
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_alumno_curso(request):
    try:
        usuario = request.user
        if not usuario.is_docente():
            return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostRegistrarAlumnoCurso(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': 'Datos ingresados incorrectos.'}, status.HTTP_400_BAD_REQUEST)
        
        data = serializer.data

        # buscar curso
        curso = Curso.objects.filter(id=data.get('id_curso')).first()
        if not curso:
            return Response({'msg': 'El curso no existe.'}, status.HTTP_404_NOT_FOUND)

        # buscar alumno
        user = User.objects.filter(username=data.get('username')).first()
        alumno = {}
        if user:
            if not user.is_alumno():
                return Response({'msg': 'El usuario no es alumno.'}, status.HTTP_400_BAD_REQUEST)
            alumno = Alumno.objects.filter(nro_documento=data.get('username')).first()
        else:
            # crear usuario
            user = User(username=data.get('username'))
            user.set_password(data.get('username'))
            user.save()
            user.groups.add(4)
            if not user.id:
                return Response({'msg': 'Error al registrar el usuario.'}, status.HTTP_400_BAD_REQUEST)
             
            # crear alumno
            alumno = Alumno(
                user=user,
                apellido_paterno=data.get('apellido_paterno'),
                apellido_materno=data.get('apellido_materno'),
                tipo_documento=data.get('tipo_documento'),
                nro_documento=data.get('username'),
            )
            alumno.save()
            if not alumno.id:
                user.delete()
                return Response({'msg': 'Error al registrar el alumno.'}, status.HTTP_400_BAD_REQUEST)

        inscripcion = AlumnoInscripcionCurso(
            alumno=alumno,
            curso=curso,
            estate = EstadoCursoInscripcion.INSCRITO
        )
        inscripcion.save()
        if not inscripcion.id:
            return Response({'msg': 'Error al registrar la inscripción.'}, status.HTTP_400_BAD_REQUEST)
        return Response({
            'msg': 'El alumno fue registrado correctamente.',
            "username": data.get('username'),
            "password": data.get('username'),
        }, status.HTTP_200_OK)
    except:
        return Response({'msg': 'Error inesperado.'}, status.HTTP_400_BAD_REQUEST)