from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Evento
from core.paginacao import resposta_paginada
from core.serializers.evento import EventoSerializer


@api_view(["GET", "POST"])
def eventos(request):
    if request.method == "GET":
        eventos = Evento.objects.all()
        categoria_id = request.query_params.get("categoria_id")
        if categoria_id:
            eventos = eventos.filter(categoria_id=categoria_id)
        organizador_id = request.query_params.get("organizador_id")
        if organizador_id:
            eventos = eventos.filter(organizador_id=organizador_id)
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
