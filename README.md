# Controle Financeiro

Aplicação web para controle financeiro pessoal, desenvolvida com Python e Flask.

O projeto está sendo construído de forma incremental, aplicando princípios de Programação Orientada a Objetos, testes automatizados, organização em camadas e boas práticas de desenvolvimento.

## Objetivo

A aplicação terá como objetivo permitir o gerenciamento e acompanhamento da vida financeira, incluindo:

- Créditos;
- Débitos;
- Categorias;
- Empréstimos;
- Parcelas;
- Dashboard financeiro;
- Comprovantes e documentos associados às movimentações.

## Tecnologias

- Python 3.14
- Flask
- Flask-SQLAlchemy
- pytest
- SQLite
- HTML
- CSS
- JavaScript
- Git
- GitHub

## Estrutura Atual

```text
controle-financeiro/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── transacao.py
│   │   ├── credito.py
│   │   ├── debito.py
│   │   └── categoria.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transacao.py
│   │   └── categoria.py
│   ├── mappers/
│   │   ├── __init__.py
│   │   ├── transacao_mapper.py
│   │   └── categoria_mapper.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── home.py
│   └── templates/
│       └── home.html
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_transacao.py
│   ├── test_credito.py
│   ├── test_debito.py
│   ├── test_categoria.py
│   ├── test_mapper.py
│   ├── test_categoria_mapper.py
│   └── test_persistencia.py
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Arquitetura: domínio e persistência separados

O projeto segue o padrão **Data Mapper**: cada conceito de negócio (`Transacao`, `Credito`, `Debito`, `Categoria`) existe em duas formas independentes:

- **`app/domain/`** — entidades de domínio, em Python puro, sem nenhuma dependência do banco de dados. Concentram as regras de negócio (validações, cálculos como `impacto_saldo()`). Podem ser testadas sem precisar de banco.
- **`app/models/`** — modelos SQLAlchemy, responsáveis apenas por como os dados são armazenados (tabelas, colunas, constraints). Não conhecem regras de negócio.
- **`app/mappers/`** — funções `to_model()` e `to_domain()` que convertem entre as duas representações.

Essa separação evita que a lógica de negócio dependa do banco de dados, e mantém os testes de domínio rápidos e independentes de infraestrutura.

### Hierarquia de domínio

```text
Transacao
├── Credito
└── Debito
```

`Credito` e `Debito` herdam de `Transacao` e implementam `impacto_saldo()` de forma polimórfica (positivo para crédito, negativo para débito). Cada uma também expõe a propriedade `tipo` (`"credito"` ou `"debito"`), usada pelo mapper para reconstruir o objeto correto ao ler do banco.

`Categoria` é uma entidade independente, com `nome` e `tipo` (`"credito"` ou `"debito"`), usada para classificar transações.

## Validações de domínio

### Transação (Crédito e Débito)

- A descrição é obrigatória e não pode conter apenas espaços;
- A categoria é obrigatória e não pode conter apenas espaços;
- O valor deve ser um `Decimal` maior que zero;
- A data deve ser um objeto `date`;
- O comprovante é opcional, mas se informado deve ser uma `str`;
- Espaços externos em descrição e categoria são removidos automaticamente.

### Categoria

- O nome é obrigatório e não pode conter apenas espaços;
- O tipo deve ser `"credito"` ou `"debito"`;
- Espaços externos no nome são removidos automaticamente.

## Persistência

A aplicação utiliza **SQLite** como banco de dados, acessado através do **SQLAlchemy** (na sintaxe declarativa tipada, com `Mapped` e `mapped_column`).

Regras de integridade garantidas pelo próprio banco:

- `transacoes.tipo` só aceita `"credito"` ou `"debito"` (`CheckConstraint`);
- `categorias.tipo` só aceita `"credito"` ou `"debito"` (`CheckConstraint`);
- não é permitido cadastrar duas categorias com o mesmo nome e o mesmo tipo (`UniqueConstraint`).

## Programação Orientada a Objetos

O projeto está sendo desenvolvido para aplicar conceitos de POO na prática, incluindo:

- Classes e objetos;
- Atributos;
- Métodos;
- Encapsulamento;
- `@property`;
- Herança;
- Abstração;
- Polimorfismo.

## Testes

Os testes automatizados são executados utilizando `pytest`.

Para executar a suíte:

```bash
pytest
```

Para executar com mais detalhes (nome de cada teste):

```bash
pytest -v
```

A suíte cobre:

- Regras de negócio do domínio (`Transacao`, `Credito`, `Debito`, `Categoria`);
- Conversão entre domínio e persistência (`mappers`);
- Gravação e leitura no banco de dados, incluindo violações de integridade (`test_persistencia.py`);
- Configuração da aplicação (`test_config.py`).

## Execução

Com o ambiente virtual ativado:

```bash
python run.py
```

A aplicação Flask estará disponível em:

```text
http://127.0.0.1:5000
```

## Status

🚧 Em desenvolvimento.

O domínio de Transação (Crédito/Débito) e Categoria já está modelado, testado e persistido em banco SQLite via SQLAlgo. O próximo passo é expor essas entidades através de rotas Flask (CRUD via HTTP).

## Próximos passos

- Criar rotas Flask (CRUD) para Categoria;
- Criar rotas Flask (CRUD) para Crédito e Débito;
- Relacionar `Transacao.categoria` à tabela `Categoria` (chave estrangeira);
- Desenvolver camada de serviços e/ou repositórios, quando justificável;
- Implementar módulo de Empréstimos e Parcelas;
- Criar dashboard financeiro;
- Ampliar cobertura de testes de rotas (integração);
- Implementar autenticação e segurança;
- Evoluir posteriormente para PostgreSQL.