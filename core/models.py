from django.db import models

TIPOS = [("participante", "participante"), ("organizador", "organizador")]
STATUS = [("pendente", "pendente"), ("confirmada", "confirmada"), ("cancelada", "cancelada")]


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nome


class Evento(models.Model):
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="eventos")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    vagas = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.titulo

    def vagas_restantes(self):
        return self.vagas - self.inscricoes.filter(status="confirmada").count()


class Inscricao(models.Model):
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="inscricoes")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="inscricoes")
    status = models.CharField(max_length=20, choices=STATUS, default="pendente")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.participante} - {self.evento}"
