from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cuestionarios.serializers import *

# *********************** DOCENTE *****************************************

"""
Soluciones de cueestionario 
"""
class SolucionCuestionarioView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # ****   id = del cuestionario   ** * ***
    def get(self, request, id):
        try:
            usuario = request.user
            # alumno
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                solucion = Solucion.objects.filter(alumno=alumno, cuestionario__id=id).first()
                serializer = SolucionSerializer(solucion)
                return Response(serializer.data, 200)
            # docente
            elif usuario.is_docente():
                data = Solucion.objects.filter(cuestionario__id=id).order_by('id').reverse()
                serializer = SolucionDocenteSerializer(data, many=True)
                return Response(serializer.data, 200)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Solucion.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)

    # metodo del docente -> id de la solucin
    def put(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                solucion = Solucion.objects.get(id=id)
                serializer = SolucionDocenteSerializer(solucion, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, 200)
                return Response(serializer.errors, 400)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Solucion.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)
    
    # metodo del docente -> id de la solucin
    def delete(self, request, id):
        try:
            usuario = request.user
            if usuario.is_docente():
                try:
                    solucion = Solucion.objects.get(id=id)
                    solucion.delete()
                    return Response({'msg': 'Eliminado'}, 200)
                except Solucion.DoesNotExist:
                    return Response({'msg': 'El cuestionario No Existe'}, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Solucion.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)


# *************************ALUMNO*************************************************

"""
Solucion de cuestionarios por parte del alumno
"""
class SolucionCursoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            usuario = request.user
            if usuario.is_alumno():
                alumno = Alumno.objects.get(user=request.user)
                solucion = Solucion.objects.filter(alumno=alumno, cuestionario__id=request.data['cuestionario_id'])
                if solucion:
                    return Response({'msg': 'Solucion ya registrada'}, 400)
                else:
                    serializer = SolucionSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(alumno=alumno)
                        return Response(serializer.data, 201)
                    return Response(serializer.errors, 404)
            else:
                return Response({'msg': 'No autorizado'}, 401)
        except Curso.DoesNotExist:
            return Response({'msg': 'El curso No Existe'}, 404)
