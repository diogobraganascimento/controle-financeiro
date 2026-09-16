"""
Testes das rotas HTTP de Categoria.
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

def test_deve_listar_categorias_quando_nao_ha_nenhuma(client):
    """
    Verifica se a página de listagem responde corretamente quando não há categorias cadastradas.
    """

    resposta = client.get("/categorias/")

    assert resposta.status_code == 200
    assert "Nenhuma categoria" in resposta.get_data(as_text=True)

def test_deve_cadastrar_categira_valida_e_redirecionar(client):
    """
    Verifica se o cadastro de uma categoria válida redireciona para a listagem, e se ela aparece lá.
    """

    resposta = client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"}
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/categorias/")

    assert "Salário" in resposta_listagem.get_data(as_text=True)

def test_nao_deve_cadastrar_categoria_com_nome_vazio(client):
    """
    Verifica se o formulário reexibe a página com o erro de domínio quando o nome está vazio.
    """

    resposta = client.post(
        "/categorias/nova",
        data={"nome": "", "tipo": "credito"},
    )

    assert resposta.status_code == 200
    assert "obrigatório" in resposta.get_data(as_text=True)

def test_nao_deve_cadastrar_categoria_duplicada(client):
    """
    VErifica se o formulário reexibe a página com o erro de duplicidade ao tentar cadastrar a mesma categoria duas vezes.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    resposta = client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    assert resposta.status_code == 200
    assert "Já existe" in resposta.get_data(as_text=True)

def test_deve_exibir_fomulario_de_edicao_preenchido(client):
    """
    verifcia se o formulário de edição vem preenchido com os dados atuais da categoria.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    categoria_id = 1  # primeira categoria criada no banco em memória

    resposta = client.get(f"/categorias/{categoria_id}/editar")

    assert resposta.status_code == 200
    assert "Salário" in resposta.get_data(as_text=True)

def test_deve_atualizar_categoria_existente(client):
    """
    Verifica se a atualização de uma categoria é persistida e reflete na listagem.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    resposta = client.post(
        "/categorias/1/editar",
        data={"nome": "Renda Extra", "tipo": "credito"},
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/categorias/")

    assert "Renda Extra" in resposta_listagem.get_data(as_text=True)
    assert "Salário" not in resposta_listagem.get_data(as_text=True)

def test_deve_excluir_categoria_existente(client):
    """
    Verifica se uma categoria excluida deixa de aparecer na listagem.
    """

    client.post(
        "/categorias/nova",
        data={"nome": "Salário", "tipo": "credito"},
    )

    resposta = client.post("/categorias/1/excluir")

    assert resposta.status_code == 302

    resposta_listagem = client.get("/categorias/")

    assert "Salário" not in resposta_listagem.get_data(as_text=True)

def test_editar_categoria_inexistente_nao_deve_quebrar(client):
    """
    Verifica se tentar editar um id inexistente não derruba a aplicação.
    """

    resposta = client.get("/categorias/999/editar")

    assert resposta.status_code == 200
    assert "não encontrada" in resposta.get_data(as_text=True)
