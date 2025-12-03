from django.db.models import *
from django.db import transaction
from dev_sistema_escolar_api.serializers import UserSerializer
from dev_sistema_escolar_api.serializers import *
from dev_sistema_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json
from django.shortcuts import get_object_or_404


class TotalEventos(generics.CreateAPIView):
    # Contar el total de cada tipo de evento
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Talleres
        talleres = Eventos.objects.filter(tipo_evento="Taller")
        total_talleres = len(talleres)

        # Seminarios
        seminarios = Eventos.objects.filter(tipo_evento="Seminario")
        total_seminarios = len(seminarios)

        # Conferencias
        conferencias = Eventos.objects.filter(tipo_evento="Conferencia")
        total_conferencias = len(conferencias)

        # Concursos
        concurso = Eventos.objects.filter(tipo_evento="Concurso")
        total_concurso = len(concurso)


        return Response(
            {
                "talleres": total_talleres,
                "seminarios": total_seminarios,
                "conferencias": total_conferencias,
                "concurso": total_concurso,
            },
            200,
        )


class EventosAll(generics.CreateAPIView):
    #Obtener todos los eventos
    # Verifica que el usuario este autenticado
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.all().order_by("id")
        lista =EventoSerializer(eventos, many=True).data
        for evento in lista:
            #JSON del publico objetivo
            if "publico_objetivo" in evento:
                try:
                    evento["publico_objetivo"] = json.loads(evento["publico_objetivo"])
                except Exception:
                    evento["publico_objetivo"] = []
            
            #JSON del programa educativo
            if "programa_educativo" in evento:
                try:
                    evento["programa_educativo"] = json.loads(evento["programa_educativo"])
                except Exception:
                    evento["programa_educativo"] = []
            if "responsable" in evento:
                try:
                    user = User.objects.get(id=evento["responsable"])
                    evento["responsable"] = f"{user.first_name} {user.last_name}"
                except Exception:
                    evento["responsable"] = "Usuario Desconocido"
        return Response(lista, 200)
            

class EventosView(generics.CreateAPIView):

    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    
    #Obtener Evento por ID
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento_obj = get_object_or_404(Eventos, id=request.GET.get("id"))
        evento_data = EventoSerializer(evento_obj, many=False).data
        if "publico_objetivo" in evento_data:
            try:
                evento_data["publico_objetivo"] = json.loads(evento_data["publico_objetivo"])
            except Exception:
                evento_data["publico_objetivo"] = []
        if "programa_educativo" in evento_data:
            try:
                evento_data["programa_educativo"] = json.loads(evento_data["programa_educativo"])
            except Exception:
                evento_data["programa_educativo"] = []
        if "responsable" in evento_data:
            try:
                user = User.objects.get(id=evento_data["responsable"])
                evento_data["responsable"] = f"{user.first_name} {user.last_name}"
            except Exception:
                evento_data["responsable"] = "Usuario Desconocido"

        return Response(evento_data, 200)
    
    #Registrar nuevo evento.
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        evento = EventoSerializer(data=data)

        if 'publico_objetivo' in data:
            data['publico_objetivo'] = json.dumps(data['publico_objetivo'])
        
        if 'programa_educativo' in data:
            data['programa_educativo'] = json.dumps(data['programa_educativo'])
        if evento.is_valid():
            responsable_user = User.objects.get(id=request.data['responsable'])
            
            evento = Eventos.objects.create(
                nombre_evento = request.data["nombre_evento"],
                tipo_evento = request.data["tipo_evento"],
                fecha = request.data['fecha'],
                hora_inicio = request.data["hora_inicio"],
                hora_fin = request.data["hora_fin"],
                lugar = request.data["lugar"],
                publico_objetivo   = json.dumps(request.data["publico_objetivo"]),
                programa_educativo = json.dumps(request.data["programa_educativo"]),
                
                descripcion = request.data["descripcion"],
                cupo = request.data["cupo"],
                
                # Asignamos el objeto de usuario real
                responsable = responsable_user
            )
            
            evento.save()
            
            return Response({"message": "Evento creado exitosamente", "id": evento.id}, 201)

        #SI EL IF FALLA (Errores de validación)
        return Response(evento.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # Verificamos que el usuario esté autenticado
        permission_classes = (permissions.IsAuthenticated,)

        data = request.data

        #Obtener el evento a actualizar
        evento = get_object_or_404(Eventos, id=data["id"])

        #Actualizar campos simples
        evento.nombre_evento = data["nombre_evento"]
        evento.tipo_evento = data["tipo_evento"]
        evento.fecha = data["fecha"]
        evento.hora_inicio = data["hora_inicio"]
        evento.hora_fin = data["hora_fin"]
        evento.lugar = data["lugar"]
        evento.descripcion = data["descripcion"]
        evento.cupo = data["cupo"]

        # 3) Campos que son listas -> se guardan como JSON (igual que en el POST)
        # Si por algo no vienen en el body, usamos lista vacía por defecto
        evento.publico_objetivo = json.dumps(data.get("publico_objetivo", []))
        evento.programa_educativo = json.dumps(data.get("programa_educativo", []))

        # 4) Actualizar responsable (User FK)
        responsable_user = get_object_or_404(User, id=data["responsable"])
        evento.responsable = responsable_user

        evento.save()

        # 6) Devolver respuesta
        return Response(
            {
                "message": "Evento actualizado correctamente",
                "evento": EventoSerializer(evento).data,
            },
            status=status.HTTP_200_OK,
        )
    
    #Eliminar Evento
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))

        try:
            evento.delete()
            return Response({"details":"Maestro eliminado"}, 200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
