# Controle Financeiro

Aplicação web para controle financeiro pessoal, desenvolvida com Python e Flask.

O projeto foi construído de forma incremental, em parceria com um assistente de IA (Claude, da Anthropic), aplicando Programação Orientada a Objetos, testes automatizados, arquitetura em camadas e boas práticas de desenvolvimento. Veja a seção **Sobre o desenvolvimento**.

## Objetivo

Permitir o gerenciamento e acompanhamento da vida financeira pessoal:

- Créditos e débitos, organizados por categoria;
- Empréstimos com cálculo automático de parcelas (Sistema Price);
- Dashboard com saldo, indicadores e gráficos;
- Relatórios financeiros mensais e anuais;
- Autenticação e proteção de acesso;
- Recorrências mensais (em desenvolvimento).

## Tecnologias

- Python 3.14
- Flask, Flask-SQLAlchemy, Flask-Login
- Werkzeug (hash de senha)
- SQLite
- pytest
- Jinja2, HTML e CSS próprio
- Chart.js (gráficos, via CDN)
- Git / GitHub

## Estrutura do Projeto

```text
controle-financeiro/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── security.py
│   ├── domain/        entidades de negócio (Python puro)
│   ├── models/        modelos SQLAlchemy
│   ├── mappers/       conversão domínio <-> persistência
│   ├── services/      orquestração dos casos de uso
│   ├── routes/        blueprints Flask
│   ├── templates/     páginas HTML (Jinja2)
│   └── static/css/    folha de estilo compartilhada
├── tests/             testes automatizados
├── docs/
│   ├── documentacao_projeto.docx
│   └── exercicios/
│       ├── exercicios.md
│       └── gabarito.md
├── requirements.txt
└── run.py
```

## Arquitetura: Data Mapper

Cada conceito de negócio pode existir em quatro camadas independentes:

- **`domain/`**: regras de negócio, validações e cálculos, em Python puro e sem dependência de banco. Testável de forma isolada.
- **`models/`**: como os dados são armazenados (tabelas, colunas, constraints, relacionamentos).
- **`mappers/`**: funções `to_model()` e `to_domain()` que convertem entre as duas representações.
- **`services/`**: casos de uso completos (criar, listar, atualizar, excluir). As rotas chamam os services e nunca acessam o banco diretamente.

```text
Transacao
├── Credito   (impacto positivo no saldo)
└── Debito    (impacto negativo no saldo)

Emprestimo   composição com uma lista de Parcela
Categoria    entidade independente (nome + tipo)
Usuario      senha sempre armazenada como hash
Recorrencia  molde de transação mensal
```

## Módulos

- **Categorias**: CRUD completo, com restrição de unicidade por nome + tipo.
- **Créditos e Débitos**: CRUD completo, vinculados a uma categoria por chave estrangeira. Compartilham uma fábrica de blueprint (`criar_blueprint_transacao`), evitando duplicação.
- **Empréstimos**: Sistema Price (parcelas fixas). Parcelas, valor final e indicadores são calculados automaticamente; cada parcela pode ser marcada como paga.
- **Dashboard**: saldo, totais e valor comprometido com empréstimos (agregações SQL), mais dois gráficos: composição créditos x débitos e evolução do saldo nos últimos 6 meses.
- **Relatórios**: mensal e anual, com agrupamento por categoria (`GROUP BY` + `extract()`).
- **Autenticação**: usuário único (Flask-Login), senha com hash, todas as rotas protegidas exceto `/login`.
- **Recorrências** *(em desenvolvimento)*: o domínio já calcula as ocorrências pendentes de uma recorrência mensal (com ajuste de dia em meses curtos, `data_fim` e pausa). Persistência e interface ainda não foram implementadas.

## Testes

```bash
pytest -v
```

Mais de 120 testes cobrindo domínio, mappers, persistência, serviços e rotas HTTP, incluindo um arquivo dedicado que reativa o login (desabilitado por padrão nos testes) para validar a proteção de acesso.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py criar-usuario seu_username
python run.py
```

A aplicação ficará em `http://127.0.0.1:5000`.

> Em produção, defina a variável de ambiente `SECRET_KEY`. O valor padrão existe apenas para desenvolvimento.

## Material didático

O projeto também serve como material de estudo de POO e lógica de programação. Em `docs/exercicios/` há:

- **`exercicios.md`**: 100 exercícios práticos em 8 blocos, do mais simples ao mais avançado, ancorados no código real do projeto (preveja a saída, encontre o bug, complete o código, implemente, explique o porquê).
- **`gabarito.md`**: respostas e explicações, em arquivo separado.

Pré-requisito: Python básico (variáveis, condicionais, laços e funções).

## Contribuições e feedback

Feedback é muito bem-vindo:

- Fez os exercícios? Abra uma *issue* contando o que achou claro, o que ficou confuso e qual foi a questão mais difícil.
- Encontrou um erro no código ou no gabarito? Abra uma *issue* ou um *pull request*.
- Tem uma ideia de melhoria ou de novo exercício? Sugira também.

## Sobre o desenvolvimento

Este projeto foi construído com o auxílio de um assistente de IA (Claude, da Anthropic), em um processo iterativo: cada funcionalidade foi precedida de explicação do conceito, seguida de implementação, testes e revisão antes do commit. Erros de código, incluindo erros de digitação na transcrição, foram depurados em conjunto como parte do aprendizado. O desenvolvedor humano validou cada etapa executando a suíte de testes.

## Status

Em desenvolvimento. A base funcional está completa.

## Próximos passos

- Recorrências: persistência, geração automática de transações e interface;
- Migrations com Alembic;
- Deploy em produção;
- Integração contínua (GitHub Actions rodando o `pytest`);
- 2FA;
- Módulo de Investimentos.