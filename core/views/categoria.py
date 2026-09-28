from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Categoria
from core.paginacao import resposta_paginada
from core.serializers.categoria import CategoriaSerializer


@api_view(["GET", "POST"])
def categorias(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        nome = request.query_params.get("nome")
        if nome:
            categorias = categorias.filter(nome__icontains=nome)
        return resposta_paginada(categorias, request, CategoriaSerializer)

    serializer = CategoriaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "GET":
        return Response(CategoriaSerializer(categoria).data)

    if request.method == "DELETE":
        if categoria.eventos.exists():
            return Response(
                {"detail": "Categoria possui eventos e nao pode ser removida"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    parcial = request.method == "PATCH"
    serializer = CategoriaSerializer(categoria, data=request.data, partial=parcial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
