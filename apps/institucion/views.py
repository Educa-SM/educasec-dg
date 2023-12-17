from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from educasm.utils.errors import NotAuthError, ServerError
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
    

# info for dashboard - docente -> login
# Institucion : #cursos, #docentes
"""
instituciones: {
    "nombre": "Institucion",
    "id": 1,
    "cursos": 10,
    "docentes": 20
}
"""
# Cuestionarios : activpos, pendientes, finalizados    
"""
cuestionario: {
    "activos": 10,
    "pendientes": 20,
    "finalizados": 30
}
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_info_dashboard_docente(request):
    try:
        usuario = request.user
        if not usuario.is_docente():
           return Response({'msg': 'No Autorizado.'}, status.HTTP_401_UNAUTHORIZED)
        instituciones = Institucion.objects.filter(docente__id=usuario.docente.id)
        """institucion = Institucion.objects.get(id=usuario.docente.institucion.id)
        cursos = Curso.objects.filter(institucion=institucion)
        cuestionarios = Cuestionario.objects.filter(curso__in=cursos)
        serializer = InstitucionSerializer(institucion)
        serializer_cuestionarios = CuestionarioDashboardSerializer(cuestionarios, many=True)
        return Response({
            'institucion': serializer.data,
            'cuestionarios': serializer_cuestionarios.data
        })"""
        data = {
            "instituciones": instituciones.count(),
        }
        return Response(data)
    except:
        raise ServerError("Error inesperado")
    pass