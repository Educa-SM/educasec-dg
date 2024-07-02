from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cuestionarios.serializers import *
from rest_framework.decorators import api_view, permission_classes
import datetime
import pytz
# BOGOTA -LIMA
time_bogota=pytz.timezone('America/Bogota')
# *********************** DOCENTE *****************************************

"""
Soluciones de cuestionario 
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

1. Iniciar solucion -> POST
2. Obtener detalle de la solucion -> GET, POST

    Solucion -> informacion de solucion numero de pregunta por donde va
    Pregunta -> cada pregunta a registrar

"""        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_evaluacion(request):
    try:
        usuario = request.user
        if usuario.is_alumno():
            alumno = Alumno.objects.get(user=request.user)
            id = request.data['cuestionario_id']
            cuestionario = Cuestionario.objects.get(id=id)
            inscripcion = AlumnoInscripcionCurso.objects.get(alumno=alumno, curso=cuestionario.curso)

            if cuestionario.fecha_asignacion > datetime.datetime.now().replace(tzinfo=time_bogota):
                return Response({'msg': 'El cuestionario aun no esta disponible'}, 400)
            
            #verificar si la solucion ya esta registrada, si no registrarla y retornar el nro de pregunta
            solucion = Solucion.objects.filter(alumno=alumno, cuestionario=cuestionario).first()
            if not solucion:
                solucion = Solucion.objects.create(alumno=alumno, cuestionario=cuestionario)
            preguntas = Pregunta.objects.filter(cuestionario=cuestionario).order_by('id')
            solucion_preguntas = SolucionPregunta.objects.filter(solucion=solucion)
            if preguntas.count() == solucion_preguntas.count():
                return Response({'msg': 'El cuestionario ya fue resuelto'}, 400)
            
            pregunta = preguntas[solucion_preguntas.count()]
            serializer = PreguntaAlumnoSerializer(pregunta)
            

            data = {
                    'total_preguntas': preguntas.count(),
                    'preguntas_resueltas': solucion_preguntas.count(),
                    'solucion_id': solucion.id,
                    'estado': solucion.estate,
                    'pregunta_siguiente': serializer.data,
                    'nro_pregunta': solucion_preguntas.count() + 1,
                }
            return Response(data, 200)
        else:
            return Response({'msg': 'No autorizado'}, 401)
    except Curso.DoesNotExist:
        return Response({'msg': 'El curso No Existe'}, 404)
    except Cuestionario.DoesNotExist:
        return Response({'msg': 'El cuestionario No Existe'}, 404)
    except AlumnoInscripcionCurso.DoesNotExist:
        return Response({'msg': 'No esta inscrito en el curso'}, 404)
    


# solucion de cada pregunta -> del alumno
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def solucion_pregunta(request):
    try:
        is_error = False
        usuario = request.user
        if usuario.is_alumno():
            alumno = Alumno.objects.get(user=request.user)

            id = request.data['solucion_id']
            solucion = Solucion.objects.get(id=id, alumno=alumno)
            if solucion.estate == EstadoSolucion.EN_REVISION:
                return Response({'msg': 'El cuestionario ya fue resuelto'}, 400)

            id = request.data['pregunta_id']
            pregunta = Pregunta.objects.get(id=id)
            solucion_pregunta = SolucionPregunta.objects.filter(solucion=solucion, pregunta=pregunta).first()
            respuesta = ""
            pregunta_solucion_id = 0
            if solucion_pregunta:
                if pregunta.intentos_disponibles <= solucion_pregunta.intentos_tomados:
                    respuesta =  'No tiene mas intentos'
                else:
                    respuesta = 'La pregunta ya fue resuelta'
                is_error = True
            else:
                solucion_data = SolucionAlumnoPreguntaSerializer(data=request.data)
                if solucion_data.is_valid():
                    tipo_pregunta = pregunta.tipo
                    opcion_pregunta = None
                    intentos_tomados = 0
                    puntaje_obtenido = 0
                    situacion_respuesta = SituacionRespuesta.PASABLE
                    if tipo_pregunta == TipoPregunta.RESPUESTA_SIMPLE:
                        intentos_tomados = 1
                        puntaje_obtenido = 0
                       
                    elif tipo_pregunta == TipoPregunta.OPCION_MULTIPLE:
                        if not 'opcion_pregunta_id' in solucion_data.data:
                            return Response({'msg': 'Debe seleccionar una opcion'}, 400)
                        opcion_pregunta = OpcionPregunta.objects.get(id=solucion_data.data['opcion_pregunta_id'], pregunta=pregunta)
                        if opcion_pregunta.correcta == SituacionPregunta.CORRECTA:
                            situacion_respuesta = SituacionRespuesta.BUENA
                            puntaje_obtenido = pregunta.puntaje_asignado
                        else:
                            situacion_respuesta = SituacionRespuesta.MALA
                            puntaje_obtenido = 0
                        intentos_tomados = 1
                    pregunta_solucion = SolucionPregunta.objects.create(
                        solucion=solucion,
                        pregunta=pregunta,
                        respuesta=solucion_data.data['respuesta'],
                        intentos_tomados=intentos_tomados,
                        puntaje_obtenido=puntaje_obtenido,
                        comentario = solucion_data.data['comentario'],
                        situacion_respuesta = situacion_respuesta
                    )
                    pregunta_solucion_id = pregunta_solucion.id
                    respuesta = "Registrada"
                else:
                    return Response(solucion_data.errors, 400)
            pregunta_siguiente = Pregunta.objects.filter(cuestionario=solucion.cuestionario, id__gt=pregunta.id).first()
            pregunta_data_next = None
            is_next = False
            if not pregunta_siguiente:
                solucion.estate = EstadoSolucion.EN_REVISION
                solucion.save()
                respuesta = "Cuestionario finalizado con exito"
                nro_pregunta = Pregunta.objects.filter(cuestionario=solucion.cuestionario).count()
            else:
                pregunta_data_next = PreguntaAlumnoSerializer(pregunta_siguiente).data
                nro_pregunta = Pregunta.objects.filter(cuestionario=solucion.cuestionario, id__lte=pregunta_siguiente.id).count()
                is_next = True

            data = {
                'nro_pregunta_siguiente': nro_pregunta,
                'pregunta_siguiente': pregunta_data_next,
                'respuesta': respuesta,
                'pregunta_solucion_id': pregunta_solucion_id,
                'is_next': is_next,
                'is_error': is_error,
                'solucion_id': solucion.id,
            }

            return Response(data, 200)

        else:
            return Response({'msg': 'No autorizado'}, 401)
    except Curso.DoesNotExist:
        return Response({'msg': 'El curso No Existe'}, 404)
    except Solucion.DoesNotExist:
        return Response({'msg': 'La Solucion No Existe'}, 404)
    except Pregunta.DoesNotExist:
        return Response({'msg': 'La pregunta No Existe'}, 404)
    except SolucionPregunta.DoesNotExist:
        return Response({'msg': 'La solucion pregunta No Existe'}, 404)
    except OpcionPregunta.DoesNotExist:
        return Response({'msg': 'La opcion pregunta No Existe'}, 404)
