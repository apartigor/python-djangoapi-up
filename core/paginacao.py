from rest_framework.pagination import PageNumberPagination


def resposta_paginada(queryset, request, serializer_class):
    paginador = PageNumberPagination()
    pagina = paginador.paginate_queryset(queryset, request)
    return paginador.get_paginated_response(serializer_class(pagina, many=True).data)
