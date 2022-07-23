from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.seguridad.serializers import UserSerializer
from .serializers import *

class NivelesView(APIView):
    def get(self, request):
        niveles = Nivel.objects.all()
        serializer_levels = NivelSerializer(niveles, many=True)
        return Response(serializer_levels.data, 201)

"""        DOCENTE       """
class CursoListView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CursoSerializer(data=request.data)
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            docente = Docente.objects.get(
                nro_documento=user_ser.data['username'])
            if serializer.is_valid():
                serializer.save(docente=docente)
                return Response(serializer.data, 201)
            return Response(serializer.errors, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


class CursoView(APIView):
    permission_classes = [IsAuthenticated]

    # id dela institucion
    def get(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                institucion = Institucion.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                cursos = Curso.objects.filter(
                    docente=docente,
                    institucion=institucion,
                    estate='A').order_by('id').reverse()
                serializer = CursoSerializer(cursos, many=True)
                return Response(serializer.data, 200)
            except Curso.DoesNotExist or Docente.DoesNotExist or Institucion.DoesNotExist:
                return Response({'msg': 'No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de Curso Docente
    def delete(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                if curso.docente == docente:
                    curso.estate = 'I'
                    curso.save()
                    return Response(status=204)
                else:
                    return Response({'msg': 'No le pertenece este curso'}, 401)
            except Curso.DoesNotExist or Docente.DoesNotExist:
                return Response({'msg': 'No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # id de Curso Docente
    def put(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                if curso.docente == docente:
                    serializer = CursoSerializer(
                        curso, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, 200)
                    return Response(serializer.errors, 404)
                else:
                    return Response({'msg': 'No le pertenece este curso'}, 401)
            except Curso.DoesNotExist or Docente.DoesNotExist:
                return Response({'msg': 'No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


class CursoIdView(APIView):
    permission_classes = [IsAuthenticated]
    # id de Curso-> Especificado
    def get(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                if curso.docente == docente or curso.estate == 'A':
                    serializer = CursoSerializer(curso)
                    return Response(serializer.data, 200)
                else:
                    return Response({'msg': 'Recurso no disponible'}, 404)
            except Curso.DoesNotExist or Docente.DoesNotExist:
                return Response({'msg': 'No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)


class CursoInscripcionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    # id del Curso retorna las inscripciones
    # id del curso inscripcion del alumno
    def get(self, request, id):
        user_ser = UserSerializer(request.user)
        # *** DOCENTE  -> id Curso
        if 2 in user_ser.data['groups']:
            try:
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                curso = Curso.objects.get(id=id, docente=docente)
                inscripciones = AlumnoInscripcionCurso.objects.filter(
                    curso_docente=curso).order_by('id').reverse()
                serializer = IncripcionCursoSerializer(
                    inscripciones, many=True)
                return Response(serializer.data, 200)
                # return Response({'msg':'ok'},200)
            except Alumno.DoesNotExist or Curso.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        elif 4 in user_ser.data['groups']:
            try:
                alumno = Alumno.objects.get(
                    nro_documento=user_ser.data['username'])
                inscripciones = AlumnoInscripcionCurso.objects.filter(
                    alumno=alumno, id=id)
                serializer = IncripcionCursoSerializer(
                    inscripciones)
                return Response(serializer.data, 200)
            except Alumno.DoesNotExist or AlumnoInscripcionCurso.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # actualizar el registro -> AlumnoInscripcionCurso : ID=> alumno Incripcion
    def put(self, request, id):
        user_ser = UserSerializer(request.user)
        if 2 in user_ser.data['groups']:
            try:
                inscripcion = AlumnoInscripcionCurso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=user_ser.data['username'])
                if inscripcion.curso_docente.docente == docente:
                    inscripcion.estate = 'D'
                    inscripcion.save()
                    return Response({'msg': 'Exito'}, 200)
                else:
                    return Response({'msg': 'No le pertenece este curso'}, 401)
            except AlumnoInscripcionCurso.DoesNotExist or Docente.DoesNotExist:
                return Response({'msg': 'No Existe'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

"""           ALUMNO         """
class CursoInscripcionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_ser = UserSerializer(request.user)
        if 4 in user_ser.data['groups']:
            try:
                alumno = Alumno.objects.get(
                    nro_documento=user_ser.data['username'])
                inscripciones = AlumnoInscripcionCurso.objects.filter(
                    alumno=alumno)
                serializer = IncripcionCursoSerializer(
                    inscripciones, many=True)
                return Response(serializer.data, 200)
            except Alumno.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    def post(self, request):
        user_ser = UserSerializer(request.user)
        if 4 in user_ser.data['groups']:
            try:
                curso_docente = Curso.objects.get(
                    codigo_inscripcion=request.data['codigo'])
                alumno = Alumno.objects.get(
                    nro_documento=user_ser.data['username'])
                if AlumnoInscripcionCurso.objects.filter(alumno=alumno,
                                                         curso_docente=curso_docente).exists():
                    return Response({'msg': 'Usted ya se a registrado a este curso'}, 400)
                else:
                    inscripcion = AlumnoInscripcionCurso(
                        alumno=alumno, curso_docente=curso_docente)
                    inscripcion.save()
                    return Response({'msg': 'Creado'}, 201)
            except Curso.DoesNotExist or Alumno.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
