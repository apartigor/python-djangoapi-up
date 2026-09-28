from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Evento
from core.filtros import filtrar_por_id
from core.paginacao import resposta_paginada
from core.serializers.evento import EventoSerializer


@api_view(["GET", "POST"])
def eventos(request):
    if request.method == "GET":
        eventos = Evento.objects.all()
        eventos = filtrar_por_id(eventos, request, "categoria_id", "categoria_id")
        eventos = filtrar_por_id(eventos, request, "organizador_id", "organizador_id")
        ativo = request.query_params.get("ativo")
        if ativo:
            eventos = eventos.filter(ativo=ativo == "true")
        return resposta_paginada(eventos, request, EventoSerializer)

    serializer = EventoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == "GET":
        return Response(EventoSerializer(evento).data)

    if request.method == "DELETE":
        evento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    parcial = request.method == "PATCH"
    serializer = EventoSerializer(evento, data=request.data, partial=parcial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
