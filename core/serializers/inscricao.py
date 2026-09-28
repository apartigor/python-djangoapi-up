from django.utils import timezone
from rest_framework import serializers

from core.models import Evento, Inscricao, Usuario
from core.serializers.evento import EventoSerializer
from core.serializers.usuario import UsuarioSerializer


class InscricaoSerializer(serializers.ModelSerializer):
    participante = UsuarioSerializer(read_only=True)
    evento = EventoSerializer(read_only=True)
    participante_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), source="participante", write_only=True
    )
    evento_id = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(), source="evento", write_only=True
    )

    class Meta:
        model = Inscricao
        fields = [
            "id", "status", "criada_em",
            "participante", "evento", "participante_id", "evento_id",
        ]

    def validate_participante_id(self, usuario):
        if usuario.tipo != "participante":
            raise serializers.ValidationError("Usuario nao e um participante")
        return usuario

    def validate(self, dados):
        if self.instance is None:
            self._validar_criacao(dados["evento"], dados["participante"])
        else:
            self._validar_atualizacao(dados)
        return dados

    def _validar_criacao(self, evento, participante):
        if not evento.ativo:
            raise serializers.ValidationError("Evento inativo")
        if evento.data <= timezone.now():
            raise serializers.ValidationError("Evento ja aconteceu")
        if evento.vagas_restantes() <= 0:
            raise serializers.ValidationError("Evento lotado")
        if Inscricao.objects.filter(
            participante=participante, evento=evento, status__in=["pendente", "confirmada"]
        ).exists():
            raise serializers.ValidationError(
                "Participante ja tem inscricao ativa neste evento"
            )

    def _validar_atualizacao(self, dados):
        if "evento" in dados and dados["evento"] != self.instance.evento:
            raise serializers.ValidationError({"evento_id": "Nao pode ser alterado"})
        if "participante" in dados and dados["participante"] != self.instance.participante:
            raise serializers.ValidationError({"participante_id": "Nao pode ser alterado"})
        if dados.get("status") == "confirmada" and self.instance.status != "confirmada":
            if self.instance.evento.vagas_restantes() <= 0:
                raise serializers.ValidationError("Evento lotado")

    def create(self, dados):
        dados["status"] = "pendente"
        return super().create(dados)
