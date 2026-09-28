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
            evento = dados["evento"]
            participante = dados["participante"]
            if evento.vagas_restantes() <= 0:
                raise serializers.ValidationError("Evento lotado")
            if Inscricao.objects.filter(
                participante=participante, evento=evento, status="pendente"
            ).exists():
                raise serializers.ValidationError(
                    "Participante ja tem inscricao pendente neste evento"
                )
        return dados

    def create(self, dados):
        dados["status"] = "pendente"
        return super().create(dados)
