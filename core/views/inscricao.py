from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Inscricao
from core.filtros import filtrar_por_id
from core.paginacao import resposta_paginada
from core.serializers.inscricao import InscricaoSerializer


@api_view(["GET", "POST"])
def inscricoes(request):
    if request.method == "GET":
        inscricoes = Inscricao.objects.all()
        inscricoes = filtrar_por_id(inscricoes, request, "participante_id", "participante_id")
        inscricoes = filtrar_por_id(inscricoes, request, "evento_id", "evento_id")
        status_da_inscricao = request.query_params.get("status")
        if status_da_inscricao:
            inscricoes = inscricoes.filter(status=status_da_inscricao)
        inscricoes = filtrar_por_id(inscricoes, request, "organizador_id", "evento__organizador_id")
        return resposta_paginada(inscricoes, request, InscricaoSerializer)

    serializer = InscricaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def inscricao(request, pk):
    inscricao = get_object_or_404(Inscricao, pk=pk)

    if request.method == "GET":
        return Response(InscricaoSerializer(inscricao).data)

    if request.method == "DELETE":
        inscricao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    parcial = request.method == "PATCH"
    serializer = InscricaoSerializer(inscricao, data=request.data, partial=parcial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
