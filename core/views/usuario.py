from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def usuarios(request):
    return Response({"detail": "Em desenvolvimento"}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def usuario(request, pk):
    return Response({"detail": "Em desenvolvimento"}, status=status.HTTP_501_NOT_IMPLEMENTED)
