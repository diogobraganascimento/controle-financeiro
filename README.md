# Controle Financeiro

Aplicação web para controle financeiro pessoal, desenvolvida com Python e Flask.

O projeto está sendo construído de forma incremental, aplicando princípios de Programação Orientada a Objetos, testes automatizados, organização em camadas e boas práticas de desenvolvimento.

## Objetivo

A aplicação terá como objetivo permitir o gerenciamento e acompanhamento da vida financeira, incluindo:

- Créditos;
- Débitos;
- Empréstimos;
- Parcelas;
- Dashboard financeiro;
- Comprovantes e documentos associados às movimentações.

## Tecnologias

- Python 3.14
- Flask
- pytest
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
- Git
- GitHub

## Estrutura Atual

controle-financeiro/
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- credito.py
|   |   |-- debito.py
|   |   |__ transacao.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |__ home.py
|   |-- templates/
|   |   |__ home.py
|-- tests/
|   |-- __init__.py
|   |-- test_credito.py
|   |__ test_debito.py
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- run.py

## Modelo de domínio

O projeto utiliza >Transacao< como classe base para representar os comportamentos e regras comuns às movimentações financeiras.

A hierarquia atual é:

transação
|-- Credito
|-- Debito

## Crédito

Um crédito representa uma entrada financeira e possui:

* Descrição;
* Valor;
* Data;
* Categoria;
* Comprovante opcional.

## Validações

Atualmente o domínio garante que:

* A descrição seja obrigatória;
* A categoria seja obrigatório;
* O valor seja um <Decimal>;
* O valor seja maior que zero;
* A data seja um objeto <date>;
* O comprovante seja um <str> ou <None>;
* Espaços externos de descrição e categoria sejam removidos.

## Programação Orientada a Objetos

O Projeto está sendo desenvolvido para aplicar conceitos de POO na prática, incluindo:

* Classes e objetos;
* Atributos;
* Métodos;
* Encapsulamento;
* @property;
* Herança;
* Abstração;
* Polimorfismo.

## Testes

Os testes automatizados são executados utilizando <pytest>.

Para executar a suíte:

pytest

Os testes verificam tanto a criação de objetos válidos quanto o tratamento de dados inválidos e as regras de negócio implementadas no domínio.

## Execução

Com o ambiente virtual ativado:

python run.py

A aplicação Flask estará disponível em:

http://127.0.0.1:5000

## Status

🚧 Em desenvolvimento.

O projeto está sendo contruído incrementalmente, começando pela modelagem do domínio e pelas regras de negócio antes da imprementação da persistência em banco de dados.

## Proxímos passos

* Refinar o modelo de domínio;
* Definir categorias;
* Implementar persistência com SQLAlchemy;
* Criar banco SQLite;
* Criar migrations;
* Implementar o CRUD;
* Desenvolver serviços e repositories;
* Implementar interface web;
* Criar dashboard financeiro;
* Ampliar cobertura de teste;
* Evoluir posteriormente para PostgreSQL.