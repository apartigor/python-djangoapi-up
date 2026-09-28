from rest_framework.exceptions import ValidationError


def filtrar_por_id(queryset, request, parametro, campo):
    valor = request.query_params.get(parametro)
    if not valor:
        return queryset
    if not valor.isdigit():
        raise ValidationError({parametro: "Deve ser um numero inteiro"})
    return queryset.filter(**{campo: int(valor)})
