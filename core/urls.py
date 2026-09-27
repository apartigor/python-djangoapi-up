from django.urls import path

from core.views import categoria, evento, health, inscricao, usuario

urlpatterns = [
    path("health/", health.health),
    path("categorias/", categoria.categorias),
    path("categorias/<int:pk>/", categoria.categoria),
    path("usuarios/", usuario.usuarios),
    path("usuarios/<int:pk>/", usuario.usuario),
    path("eventos/", evento.eventos),
    path("eventos/<int:pk>/", evento.evento),
    path("inscricoes/", inscricao.inscricoes),
    path("inscricoes/<int:pk>/", inscricao.inscricao),
]
