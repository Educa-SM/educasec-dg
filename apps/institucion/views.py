from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from educasm.utils.errors import NotAuthError, ServerError

class InstitucionesView(APIView):
    def get(self, request):
        instituciones = Institucion.objects.all()
        serializer = InstitucionSerializer(instituciones, many=True)
        return Response(serializer.data)
    
class MensajeInicioView(APIView):
    def get(self, request):
        try:
            usuario = request.user
            if not  usuario.is_admin_recursos():
                raise NotAuthError("No autorizado")
            mensajes = MensajeInicio.objects.all()
            serializer = MensajeInicioSerializer(mensajes, many=True)
            return Response(serializer.data)   
        except:
            raise ServerError("Error inesperado")
    
    def post(self, request):
        try:
            usuario = request.user
            if not usuario.is_admin_recursos():
                raise NotAuthError("No autorizado")
            serializer = MensajeInicioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            raise ServerError("Datos invalidos")
        except:
            raise ServerError("Error inesperado")
    
class MensajeInicioDetailView(APIView):
    def put(self, request, id):
        try:
            usuario = request.user
            if not usuario.is_admin_recursos():
                raise NotAuthError("No autorizado")
            mensaje = MensajeInicio.objects.get(id=id)
            serializer = MensajeInicioSerializer(mensaje, data=request.data)
            if serializer.is_valid():
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
