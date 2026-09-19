"""
Testes das rotas HTTP de Crédito.
"""

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    """
    Cria um cliente de teste Flask com banco em memória.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory",
        }
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()

def test_deve_listar_creditos_quando_nao_ha_nenhum(client):
    """
    Verifica se a página de listagem responde corretamente quando não há créditos cadastrados.
    """

    resposta = client.get("/creditos/")

    assert resposta.status_code == 200
    assert "Nenhum crédito" in resposta.get_data(as_text=True)

def test_formulario_deve_orientar_a_cadastrar_categoria_primeiro(client):
    """
    Verifica se o formulário de novo crédito orienta o usuário a cadastrar uma categoria quando não há nenhuma do tipo credito.
    """

    resposta = client.get("/creditos/novo")

    assert resposta.status_code == 200
    assert "Cadastrar categoria primeiro" in resposta.get_data(as_text=True)

def test_deve_cadastrar_credito_valido_e_redirecionar(client):
    """
    Verifica se o cadastro de um crédito válido redireciona para a listagem, e se ele aparece lá.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"}
    )

    resposta = client.post(
        "/creditos/novo",
        data={
            "descricao": "Salário de Setembro",
            "valor": "5000.00",
            "data": "2026-09-05",
            "categoria": "Salário",
        },
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/creditos/")

    assert "Salário de Setembro" in resposta_listagem.get_data(as_text=True)

def test_nao_deve_cadastrar_credito_com_valor_invalido(client):
    """
    Verifica se um valor não numérico é rejeitado com mensagem amigável, sem quebrar a aplicação.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    resposta = client.post(
        "/creditos/novo",
        data={
            "descricao": "Salário",
            "valor": "abc",
            "data": "2026-09-05",
            "categoria": "Salário",
        },
    )

    assert resposta.status_code == 200
    assert "valor inválido" in resposta.get_data(as_text=True)

def test_nao_deve_cadastrar_credito_com_data_invalida(client):
    """
    Verifica se uma data em formato inválido é rejeitada com mensagem amigável.
    """

    client.post(
        "/categoria/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    resposta = client.post(
        "/creditos/novo",
        data={
            "descricao": "Salário",
            "valor": "5000.00",
            "data": "05/09/2026",
            "categoria": "Salário",
        },
    )

    assert resposta.status_code == 200
    assert "Data inválida" in resposta.get_data(as_text=True)

def test_nao_deve_cadastrar_credito_com_categoria_inexistente(client):
    """
    Verifica se o formulário rejeita uma categoria que não está cadastrada.
    """

    resposta = client.post(
        "/creditos/novo",
        data={
            "descricao": "Salário",
            "valor": "5000.00",
            "data": "2026-09-05",
            "categoria": "Categoria Fantasma",
        },
    )

    assert resposta.status_code == 200
    assert "não está cadastrada" in resposta.get_data(as_text=True)
