from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
        usuario = request.user
        if usuario.is_docente():
            docente = Docente.objects.get(
                nro_documento=usuario.username)
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
        usuario = request.user
        if usuario.is_docente():
            try:
                institucion = Institucion.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
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
        usuario = request.user
        if usuario.is_docente():
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
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
        usuario = request.user
        if usuario.is_docente():
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
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
        usuario = request.user
        if usuario.is_docente():
            try:
                curso = Curso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
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
        usuario = request.user
        # *** DOCENTE  -> id Curso
        if usuario.is_docente():
            try:
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
                curso = Curso.objects.get(id=id, docente=docente)
                inscripciones = AlumnoInscripcionCurso.objects.filter(
                    curso=curso).order_by('id').reverse()
                serializer = IncripcionCursoDocenteSerializer(
                    inscripciones, many=True)
                return Response(serializer.data, 200)
                # return Response({'msg':'ok'},200)
            except Alumno.DoesNotExist or Curso.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        elif usuario.is_alumno():
            
            try:
                alumno = Alumno.objects.get(
                    nro_documento=usuario.username)
                curso = Curso.objects.get(id=id)
               
                inscripciones = AlumnoInscripcionCurso.objects.filter(
                    alumno=alumno, curso=curso).first()
                serializer = IncripcionCursoSerializer(
                    inscripciones)
                return Response(serializer.data, 200)
            except Alumno.DoesNotExist or AlumnoInscripcionCurso.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)

    # actualizar el registro -> AlumnoInscripcionCurso : ID=> alumno Incripcion
    def put(self, request, id):
        usuario = request.user
        if usuario.is_docente():
            try:
                inscripcion = AlumnoInscripcionCurso.objects.get(id=id)
                docente = Docente.objects.get(
                    nro_documento=usuario.username)
                if inscripcion.curso.docente == docente:
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
        usuario = request.user
        if usuario.is_alumno():
            try:
                alumno = Alumno.objects.get(
                    nro_documento=usuario.username)
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
        usuario = request.user
        if usuario.is_alumno():
            try:
                curso = Curso.objects.get(
                    codigo_inscripcion=request.data['codigo'])
                alumno = Alumno.objects.get(
                    nro_documento=usuario.username)
                if AlumnoInscripcionCurso.objects.filter(alumno=alumno,
                                                         curso=curso).exists():
                    return Response({'msg': 'Usted ya se a registrado a este curso'}, 400)
                else:
                    inscripcion = AlumnoInscripcionCurso(
                        alumno=alumno, curso=curso)
                    inscripcion.save()
                    return Response({'msg': 'Creado'}, 201)
            except Curso.DoesNotExist or Alumno.DoesNotExist:
                return Response({'msg': 'No Existe el curso'}, 404)
        else:
            return Response({'msg': 'No autorizado'}, 401)
