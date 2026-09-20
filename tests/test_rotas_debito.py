"""
Testes das rotas HTTP de Débito.
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
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()

def test_deve_listar_debitos_quando_nao_ha_nenhum(client):
    """
    Verifica se a página de listagem responde corretamente
    quando não há débitos cadastrados.
    """

    resposta = client.get("/debitos/")

    assert resposta.status_code == 200
    assert "Nenhum débito" in resposta.get_data(as_text=True)

def test_deve_cadastrar_debito_valido_e_redirecionar(client):
    """
    Verifica se o cadastro de um débito válido redireciona
    para a listagem, e se ele aparece lá.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Moradia", "tipo": "debito"},
    )

    resposta = client.post(
        "/debitos/novo",
        data={
            "descricao": "Aluguel",
            "valor": "1800.00",
            "data": "2026-09-10",
            "categoria": "Moradia",
        },
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/debitos/")

    assert "Aluguel" in resposta_listagem.get_data(as_text=True)

def test_creditos_e_debitos_devem_ficar_em_listas_separadas(client):
    """
    Verifica se um crédito não aparece na listagem de débitos
    e vice-versa, mesmo compartilhando a mesma tabela no banco.
    """

    client.post("/categorias/nova", data={"nome": "Salário", "tipo": "credito"})
    client.post("/categorias/nova", data={"nome": "Moradia", "tipo": "debito"})

    client.post(
        "/creditos/novo",
        data={
            "descricao": "Salário",
            "valor": "5000.00",
            "data": "2026-09-05",
            "categoria": "Salário",
        },
    )
    client.post(
        "/debitos/novo",
        data={
            "descricao": "Aluguel",
            "valor": "1800.00",
            "data": "2026-09-10",
            "categoria": "Moradia",
        },
    )

    resposta_creditos = client.get("/creditos/")
    resposta_debitos = client.get("/debitos/")

    assert "Salário" in resposta_creditos.get_data(as_text=True)
    assert "Aluguel" not in resposta_creditos.get_data(as_text=True)

    assert "Aluguel" in resposta_debitos.get_data(as_text=True)
    assert "Salário" not in resposta_debitos.get_data(as_text=True)

def test_deve_atualizar_debito_existente(client):
    """
    Verifica se a atualização de um débito é persistida
    e reflete na listagem.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Moradia", "tipo": "debito"},
    )
    client.post(
        "/debitos/novo",
        data={
            "descricao": "Aluguel",
            "valor": "1800.00",
            "data": "2026-09-10",
            "categoria": "Moradia",
        },
    )

    resposta = client.post(
        "/debitos/1/editar",
        data={
            "descricao": "Aluguel Reajustado",
            "valor": "1900.00",
            "data": "2026-10-10",
            "categoria": "Moradia",
        },
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/debitos/")

    assert "Aluguel Reajustado" in resposta_listagem.get_data(as_text=True)

def test_deve_excluir_debito_existente(client):
    """
    Verifica se um débito excluído deixa de aparecer
    na listagem.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Moradia", "tipo": "debito"},
    )
    client.post(
        "/debitos/novo",
        data={
            "descricao": "Aluguel",
            "valor": "1800.00",
            "data": "2026-09-10",
            "categoria": "Moradia",
        },
    )

    resposta = client.post("/debitos/1/excluir")

    assert resposta.status_code == 302

    resposta_listagem = client.get("/debitos/")

    assert "Aluguel" not in resposta_listagem.get_data(as_text=True)
