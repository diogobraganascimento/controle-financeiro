# Controle Financeiro

Aplicação web para controle financeiro pessoal, desenvolvida com Python e Flask.

O projeto foi construído de forma incremental, em pareceria com um assistente de IA (Claude, da Anthropic), aplicando princípios de Programação Orientada a Objetos, testes automatizados, organização em camadas e boas práticas de desenvolvimento. Veja a seção **Sobre o desenvolvimento** para mais detalhes sobre essa metodologia.

## Objetivo

Permitir o gerenciamento e acompanhamento completo da vida financeira pessoal:

- Créditos e débitos, organizados por categoria;
- Empréstimos com cálculo automático de parcelas (Sistema Price);
- Dashboard com saldo e indicadores consolidados;
- Relatórios financeiros mensais e anuais;
- Autenticação e proteção de acesso.

Investimentos, autenticação em duas etapas (2FA) e deploy em produção são evoluções futuras planejadas.

## Tecnologias

- Python 3.14
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug (hash de senha)
- pytest
- SQLite
- HTML, CSS (folha de estilo própria, sem frameworks)
- Jinja2
- Git / GitHub

## Estrutura do Projeto

```text
controle-financeiro/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── security.py
│   ├── domain/
│   │   ├── transacao.py
│   │   ├── credito.py
│   │   ├── debito.py
│   │   ├── categoria.py
│   │   ├── emprestimo.py
│   │   ├── parcela.py
│   │   └── usuario.py
│   ├── models/
│   │   ├── transacao.py
│   │   ├── categoria.py
│   │   ├── emprestimo.py
│   │   ├── parcela.py
│   │   └── usuario.py
│   ├── mappers/
│   │   ├── transacao_mapper.py
│   │   ├── categoria_mapper.py
│   │   ├── emprestimo_mapper.py
│   │   └── usuario_mapper.py
│   ├── services/
│   │   ├── categoria_service.py
│   │   ├── transacao_service.py
│   │   ├── emprestimo_service.py
│   │   ├── dashboard_service.py
│   │   ├── relatorio_service.py
│   │   └── auth_service.py
│   ├── routes/
│   │   ├── home.py
│   │   ├── auth.py
│   │   ├── categoria.py
│   │   ├── credito.py
│   │   ├── debito.py
│   │   ├── transacao_routes.py     (fábrica de blueprint)
│   │   ├── emprestimo.py
│   │   └── relatorio.py
│   ├── templates/
│   │   ├── home.html
│   │   ├── auth/login.html
│   │   ├── categorias/ (listar, nova, editar)
│   │   ├── creditos/   (listar, nova, editar)
│   │   ├── debitos/    (listar, nova, editar)
│   │   ├── emprestimos/ (listar, novo, detalhe)
│   │   └── relatorios/ (index, mensal, anual)
│   └── static/
│       └── css/style.css
├── tests/                          (123 testes)
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Arquitetura: domínio e persistência separados (Data Mapper)

Cada conceito de negócio existe em até três formas independentes:

- **`app/domain/`** — entidades em Python puro, sem nenhuma dependência do banco. Concentram as regras de negócio (validações, cálculos como `impacto_saldo()` e a fórmula do Sistema Price). Testadas sem precisar de banco de dados.
- **`app/models/`** — modelos SQLAlchemy, responsáveis apenas por como os dados são armazenados (tabelas, colunas, constraints, relacionamentos).
- **`app/mappers/`** — funções `to_model()` e `to_domain()` que convertem entre as duas representações.
- **`app/services/`** — orquestram casos de uso completos (criar, listar, atualizar, excluir), conectando domínio, mapper e persistência. É a camada que as rotas Flask chamam — elas nunca falam diretamente com o banco.

### Hierarquia de domínio

```text
Transacao
├── Credito   (impacto positivo no saldo)
└── Debito    (impacto negativo no saldo)

Emprestimo  — composição com uma lista de Parcela
Categoria   — entidade independente (nome + tipo)
Usuario     — senha sempre armazenada como hash (nunca texto puro)
```

## Módulos

### Categorias
CRUD completo (criar, listar, editar, excluir), com `tipo` (`credito`/`debito`) e restrição de unicidade por nome+tipo.

### Créditos e Débitos
CRUD completo, vinculados a uma `Categoria` real via chave estrangeira (`categoria_id`). As rotas de Crédito e Débito compartilham a mesma fábrica de blueprint (`criar_blueprint_transacao`), evitando duplicação de código entre as duas.

### Empréstimos
Calculados pelo **Sistema Price** (parcelas fixas): o valor da parcela, o valor final e a lista completa de parcelas são gerados automaticamente a partir do valor retirado, da taxa de juros mensal e da quantidade de parcelas. Cada parcela pode ser marcada como paga individualmente. `Emprestimo` e `Parcela` têm uma relação um-para-muitos com exclusão em cascata (`cascade="all, delete-orphan"`).

### Dashboard
Página inicial com saldo atual, totais de crédito/débito e valor comprometido com empréstimos em aberto, calculados com funções de agregação SQL (`SUM`, `COUNT`).

### Relatórios
Relatório mensal e anual, com totais e agrupamento por categoria, usando `GROUP BY` e `extract()` para filtrar por período.

### Autenticação
Sistema de usuário único (Flask-Login), com senha sempre hasheada (`werkzeug.security`). Todas as rotas exigem login, exceto `/login`. O usuário é criado via comando de terminal (`flask criar-usuario`), sem cadastro público.

## Persistência

**SQLite**, acessado via SQLAlchemy (sintaxe declarativa tipada, `Mapped`/`mapped_column`). Integridade garantida pelo próprio banco:

- `transacoes.tipo` e `categorias.tipo` só aceitam `"credito"` ou `"debito"` (`CheckConstraint`);
- Não é permitido cadastrar duas categorias com o mesmo nome e tipo (`UniqueConstraint`);
- `transacoes.categoria_id` e `parcelas.emprestimo_id` são chaves estrangeiras reais;
- Excluir um empréstimo exclui automaticamente suas parcelas.

## Testes

```bash
pytest -v
```

**123 testes**, cobrindo domínio, mappers, persistência, serviços e rotas HTTP (incluindo autenticação, com um arquivo dedicado que reativa a proteção de login para validá-la de verdade).

## Execução

```bash
python run.py
```

Antes do primeiro acesso, crie o usuário do sistema:

```bash
flask --app run.py criar-usuario seu_username
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

## Sobre o desenvolvimento

Este projeto foi construído inteiramente através de pareamento com um assistente de IA (Claude, Anthropic), em um processo iterativo e didático: cada funcionalidade foi precedida de explicação de conceito, seguida de implementação, teste e revisão antes do commit. Erros de código (incluindo erros de digitação introduzidos na hora de transcrever o código) foram depurados em conjunto, como parte do processo de aprendizado. Veja `documentacao_projeto.docx` para mais detalhes sobre essa metodologia.

## Status

🚧 Em desenvolvimento — base funcional completa.

## Próximos passos

- Autenticação em duas etapas (2FA);
- Módulo de Investimentos;
- Melhorias de UX/UI;
- Deploy em produção.
