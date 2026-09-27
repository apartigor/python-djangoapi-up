# API de Eventos e Inscrições

Trabalho de Tópicos Especiais em Software - Prof. Rhafael Freitas da Costa.
API RESTful feita em Python com Django e Django REST Framework.

Plataforma onde organizadores publicam eventos por categoria e participantes se inscrevem neles, com o organizador confirmando ou cancelando cada inscrição.

## Como rodar

1. Criar o ambiente virtual:

   ```bash
   python -m venv venv
   ```

2. Ativar o ambiente virtual:

   ```bash
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux / macOS
   ```

3. Instalar as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Criar o arquivo de configuração (o `.env` guarda a `SECRET_KEY`, o `DEBUG`, os hosts permitidos e o nome do banco):

   ```bash
   copy .env.example .env       # Windows
   cp .env.example .env         # Linux / macOS
   ```

5. Rodar as migrações e cadastrar as categorias:

   ```bash
   python manage.py migrate
   python seed.py
   ```

6. Iniciar o servidor:

   ```bash
   python manage.py runserver
   ```

   Para conferir se a API subiu, acesse `http://127.0.0.1:8000/api/health/`, que responde `{"status": "ok"}`.
