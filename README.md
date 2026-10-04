# Mundo dos Números

MVP educativo infantil em português brasileiro para crianças de 6 a 9 anos. Responsáveis criam contas e perfis infantis; as crianças praticam matemática em trilhas curtas. O projeto usa Django, templates nativos e regras matemáticas determinísticas no servidor.

## Tecnologias

- Python 3.13 (compatível com Django 5.2 LTS)
- Django, SQLite local e PostgreSQL em produção
- WhiteNoise, Gunicorn com Uvicorn Worker e `dj-database-url`
- HTML, CSS, JavaScript sem framework e PWA
- Google Gen AI SDK opcional para narração

## Instalação no Windows 11

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_initial_curriculum
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. Para criar conteúdo no Admin: `python manage.py createsuperuser`.

## Testes e verificações

```powershell
python manage.py test
python manage.py check
python manage.py makemigrations --check
python manage.py collectstatic --noinput
```

## Gemini e voz

Gemini é opcional: a matemática e o progresso não dependem dele. Copie `.env.example` para `.env` e ajuste `ENABLE_GEMINI=True` apenas depois de configurar `GEMINI_API_KEY` localmente. Nunca versione esse arquivo. Use `python manage.py generate_lesson_audio` para gerar áudio previamente; o comando ignora arquivos já existentes e falha de forma segura sem chave.

## Render

Use o Blueprint em `render.yaml` ou crie manualmente um Web Service e PostgreSQL. Configure `ENVIRONMENT=production`, `DEBUG=False`, `SECRET_KEY`, `DATABASE_URL` e `ALLOWED_HOSTS`. O build é `bash build.sh`; o início é:

```text
python -m gunicorn mundo_numeros.asgi:application -k uvicorn.workers.UvicornWorker
```

Cadastre as variáveis Gemini protegidas somente no painel do Render, se for usar IA. O plano gratuito pode suspender o serviço após inatividade; este projeto não tenta contornar isso.

## Problemas comuns

- **Sem lições:** execute `python manage.py seed_initial_curriculum`.
- **Erro de banco no Render:** confirme que `DATABASE_URL` está vinculada ao banco criado pelo Blueprint.
- **Áudio indisponível:** mantenha Gemini desativado; o texto e o fallback de navegador continuam disponíveis.
- **Estáticos ausentes em produção:** execute `collectstatic` pelo `build.sh`.
