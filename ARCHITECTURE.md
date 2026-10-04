# Arquitetura

O projeto Django é dividido em `accounts`, `curriculum`, `learning`, `gamification`, `ai_voice` e `core`. Nesta fundação, `accounts` protege as contas dos responsáveis, `core` entrega páginas públicas e saúde, e as demais apps serão preenchidas nas próximas fases.

As requisições entram pelas URLs Django, passam por CSRF/autenticação e chegam a views e templates. Em desenvolvimento o banco é SQLite; com `DATABASE_URL`, usa-se PostgreSQL. Regras de aprendizagem e pontuação ficarão no servidor.

Em produção WhiteNoise serve estáticos e as configurações forçam HTTPS, HSTS e cookies seguros.
