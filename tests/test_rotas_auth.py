"""
Testes das rotas de autenticação e da proteção de acesso.

Diferente dos demais arquivos de teste, aqui passamos
"LOGIN_DISABLED": False explicitamente, porque o objetivo destes
testes é justamente confirmar que a proteção de login funciona.
"""

import pytest

from app import create_app
from app.extensions import db
from app.services.auth_service import criar_usuario


@pytest.fixture
def client():
    """
    Cria um cliente de teste Flask com banco em memória e a autenticação ativada, com 
    um usuário já cadastrado.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "LOGIN_DISABLED": False,
        }
    )

    with app.app_context():
        db.create_all()
        criar_usuario("dnascimento", "senha1234")

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()

def test_rota_protegida_deve_redirecionar_sem_login(client):
    """
    Verifica se acessar uma rota protegida sem estar logado redireciona para a
    página de login.
    """

    resposta = client.get("/categorias/")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]

def test_login_com_credenciais_corretas_deve_redirecionar(client):
    """
    Verifica se um login válido redireciona para a página inicial.
    """

    resposta = client.post(
        "/login",
        data={"username": "dnascimento", "senha": "senha1234"},
    )

    assert resposta.status_code == 302

def test_login_com_senha_incorreta_deve_reexibir_formulario(client):
    """
    Verifica se um login inválido reexibe o formulário com mensagem de erro.
    """

    resposta = client.post(
        "/login",
        data={"username": "dnascimento", "senha": "errada"},
    )

    assert resposta.status_code == 200
    assert "inválidos" in resposta.get_data(as_text=True)

def test_rota_protegida_deve_funcionar_apos_login(client):
    """
    Verficar se, após o login, uma rota antes protegida passa a responder normalmente.
    """

    client.post(
        "/login",
        data={"username": "dnascimento", "senha": "senha1234"},
    )

    resposta = client.get("/categorias/")

    assert resposta.status_code == 200

def test_logout_deve_bloquear_acesso_novamente(client):
    """
    Verifica se, após logout, o acesso a uma rota protegida volta a ser bloqueada.
    """

    client.post(
        "/login",
        data={"username": "dnascimento", "senha": "senha1234"},
    )

    client.post("/logout")

    resposta = client.get("/categorias/")

    assert resposta.status_code == 302
