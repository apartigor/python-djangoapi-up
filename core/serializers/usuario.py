from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nome", "email", "senha", "tipo", "criado_em"]
        extra_kwargs = {"senha": {"write_only": True}}

    def validate_senha(self, senha):
        return make_password(senha)
