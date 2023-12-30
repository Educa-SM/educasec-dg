from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from educasm.utils.errors import NotAuthError, ServerError
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.cursos.models import Curso
from apps.cuestionarios.models import Cuestionario, Pregunta

class InstitucionesView(APIView):
    def get(self, request):
        instituciones = Institucion.objects.all()
        serializer = InstitucionSerializer(instituciones, many=True)
        return Response(serializer.data)
    
class MensajeInicioView(APIView):
    def get(self, request):
        usuario = request.user
        if not  usuario.is_admin_recursos():
            raise NotAuthError("No autorizado")
        try:
            mensajes = MensajeInicio.objects.all()
            serializer = MensajeInicioSerializer(mensajes, many=True)
            return Response(serializer.data)   
        except:
            raise ServerError("Error inesperado")
    
    def post(self, request):
        usuario = request.user
        if not usuario.is_admin_recursos():
            raise NotAuthError("No autorizado")
        try:
            serializer = MensajeInicioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(usuario=usuario)
                return Response(serializer.data)
            raise ServerError("Datos invalidos")
        except:
            raise ServerError("Error en Datos")
    
class MensajeInicioDetailView(APIView):
    def put(self, request, id):
        usuario = request.user
        if not usuario.is_admin_recursos():
            raise NotAuthError("No autorizado")
        try:
            mensaje = MensajeInicio.objects.get(id=id)
            serializer = MensajeInicioSerializer(mensaje, data=request.data)
            if serializer.is_valid():
                if 'imagen' in serializer.validated_data:
                    mensaje.imagen.delete()
                serializer.save()
                return Response(serializer.data)
            raise ServerError("Datos invalidos")
        except:
            raise ServerError("Error inesperado")
    
    def delete(self, request, id):
        try:
            usuario = request.user
            if not usuario.is_admin_recursos():
                raise NotAuthError("No autorizado")
            mensaje = MensajeInicio.objects.get(id=id)
            mensaje.delete()
            return Response('Mensaje eliminado')
        except:
            raise ServerError("Error inesperado")
        
class MensajesHoyView(APIView):
    def get(self, request):
        try:
            # query django for compare fecha inicio y fecha fin con la fecha actual
            fecha_actual = datetime.date.today()
            mensajes = MensajeInicio.objects.filter(fecha_inicio__lte=fecha_actual, fecha_fin__gte=fecha_actual)
            serializer = MensajeInicioPublicoSerializer(mensajes, many=True)
            return Response(serializer.data)
        except:
            raise ServerError("Error inesperado")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_docentes_pendientes(request):
    try:
        usuario = request.user
        if not usuario.is_admin_recursos():
           return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        docentes = Docente.objects.filter(estate='P')
        serializer = DocenteSerializer(docentes, many=True)
        return Response(serializer.data)
    except:
        raise ServerError("Error inesperado")
    

# info for dashboard - docente
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_info_dashboard_docente(request):
    try:
        usuario = request.user
        if not usuario.is_docente():
           return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        instituciones = Institucion.objects.filter(docente__id=usuario.docente.id)
        data_instituciones = []

        num_empezar = 0
        num_finalizados = 0
        num_activos = 0
        date_now = datetime.datetime.now().timestamp()
        
        for institucion in instituciones:
            cursos = Curso.objects.filter(
                institucion__id=institucion.id,  docente__id=usuario.docente.id
            )
            cuestionarios = Cuestionario.objects.filter(
                curso__in=cursos, estate='A'
            )
            for cuestionario in cuestionarios:
                if cuestionario.fecha_asignacion.timestamp() > date_now:
                    num_empezar += 1
                elif cuestionario.fecha_expiracion.timestamp() < date_now:
                    num_finalizados += 1
                else:
                    num_activos += 1

            num_preguntas = Pregunta.objects.filter(
                cuestionario__in=cuestionarios, estate='A'
            ).count()

            data_instituciones.append({
                "nombre": institucion.nombre,
                "id": institucion.id,
                "cursos": cursos.count(),
                "cuestionarios": cuestionarios.count(),
                "preguntas": num_preguntas,
            })

        data_cuestionarios = {
            "empezar" : num_empezar,
            "activos" : num_activos,
            "finalizados" : num_finalizados
        }

        data = {
            "instituciones": data_instituciones,
            "cuestionarios": data_cuestionarios,
        }
        return Response(data)
    except:
        raise ServerError("Error inesperado")