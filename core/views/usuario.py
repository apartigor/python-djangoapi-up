from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Usuario
from core.paginacao import resposta_paginada
from core.serializers.usuario import UsuarioSerializer


@api_view(["GET", "POST"])
def usuarios(request):
    if request.method == "GET":
        usuarios = Usuario.objects.all()
        tipo = request.query_params.get("tipo")
        if tipo:
            usuarios = usuarios.filter(tipo=tipo)
        return resposta_paginada(usuarios, request, UsuarioSerializer)

    serializer = UsuarioSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "GET":
        return Response(UsuarioSerializer(usuario).data)

    if request.method == "DELETE":
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    parcial = request.method == "PATCH"
    serializer = UsuarioSerializer(usuario, data=request.data, partial=parcial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
