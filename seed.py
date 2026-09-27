import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Categoria

NOMES_DAS_CATEGORIAS = ["Tecnologia", "Negócios", "Saúde e bem-estar", "Arte e cultura", "Esporte"]

for nome in NOMES_DAS_CATEGORIAS:
    categoria, criada = Categoria.objects.get_or_create(nome=nome)
    if criada:
        print(f"Categoria criada: {nome}")
    else:
        print(f"Categoria já existe: {nome}")

print(f"Total de categorias: {Categoria.objects.count()}")
