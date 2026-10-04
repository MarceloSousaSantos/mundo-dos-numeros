# Decisões Técnicas

- **Django 5.2 LTS:** compatível com Python 3.13 instalado e com suporte estendido.
- **Custom User com e-mail:** criado antes da primeira migração para evitar migração futura de autenticação.
- **Templates nativos:** mantém o MVP didático e sem frontend separado.
- **SQLite local / PostgreSQL por `DATABASE_URL`:** desenvolvimento simples e produção preparada.
- **Gemini opcional:** a aplicação central não pode depender de IA ou expor credenciais.
