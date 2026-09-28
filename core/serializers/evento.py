from rest_framework import serializers

from core.models import Categoria, Evento, Usuario
from core.serializers.categoria import CategoriaSerializer
from core.serializers.usuario import UsuarioSerializer


class EventoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    organizador = UsuarioSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source="categoria", write_only=True
    )
    organizador_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source="organizador", write_only=True
    )
    vagas_restantes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Evento
        fields = [
            "id", "titulo", "descricao", "data", "local", "vagas",
            "vagas_restantes", "preco", "ativo",
            "categoria", "organizador", "categoria_id", "organizador_id",
        ]

    def validate_organizador_id(self, usuario):
        if usuario.tipo != "organizador":
            raise serializers.ValidationError("Usuario nao e um organizador")
        return usuario
