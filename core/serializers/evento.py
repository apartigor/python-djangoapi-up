from django.utils import timezone
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

    def validate_vagas(self, vagas):
        if vagas < 1:
            raise serializers.ValidationError("Deve haver pelo menos 1 vaga")
        return vagas

    def validate_preco(self, preco):
        if preco < 0:
            raise serializers.ValidationError("Preco nao pode ser negativo")
        return preco

    def validate_data(self, data):
        mudou = self.instance is None or data != self.instance.data
        if mudou and data <= timezone.now():
            raise serializers.ValidationError("Data deve ser no futuro")
        return data

    def validate(self, dados):
        vagas = dados.get("vagas")
        if self.instance is not None and vagas is not None:
            confirmadas = self.instance.inscricoes.filter(status="confirmada").count()
            if vagas < confirmadas:
                raise serializers.ValidationError(
                    {"vagas": f"Evento ja tem {confirmadas} inscricoes confirmadas"}
                )
        return dados
