
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('senha', models.CharField(max_length=128)),
                ('tipo', models.CharField(choices=[('participante', 'participante'), ('organizador', 'organizador')], max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True)),
                ('data', models.DateTimeField()),
                ('local', models.CharField(max_length=200)),
                ('vagas', models.PositiveIntegerField()),
                ('preco', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('ativo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eventos', to='core.categoria')),
                ('organizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='core.usuario')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pendente', 'pendente'), ('confirmada', 'confirmada'), ('cancelada', 'cancelada')], default='pendente', max_length=20)),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='core.evento')),
                ('participante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscricoes', to='core.usuario')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
