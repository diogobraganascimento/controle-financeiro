"""
Teste das rotas HTTP de Emprestimo.
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

def test_deve_listar_emprestimos_quando_nao_ha_nenhum(client):
    """
    Verifica se a página de listagem responde corretamente quando não há empréstimos cadastrados.
    """

    resposta = client.get("/emprestimos/")

    assert resposta.status_code == 200
    assert "Nenhum empréstimo" in resposta.get_data(as_text=True)

def test_cadastrar_emprestimo_valido_e_redirecionar(client):
    """
    Verifica se o cadastro de um empréstimo válido redireciona para a listagem, e se ele aparece lá com suas parcelas.
    """

    resposta = client.post(
        "/emprestimos/novo",
        data={
            "descricao": "Empréstimo pessoal",
            "valor_retirado": "5000.00",
            "taxa_juros_mensal": "2",
            "quantidade_parcelas": "12",
            "idade_parcelas": "12",
            "data_contratacao": "2026-09-01",
        },
    )

    assert resposta.status_code == 302

    resposta_listagem = client.get("/emprestimos/")

    assert "Empréstimo pessoal" in resposta_listagem.get_data(as_text=True)
    assert "0/12 parcelas pagas" in resposta_listagem.get_data(as_text=True)

def test_deve_exibir_detalhe_com_parcelas(client):
    """
    Verifica se a página de detalhe exibe todas as parcelas do empréstimo.
    """

    client.post(
        "/emprestimos/novo",
        data={
            "descricao": "Empréstimo pessoal",
            "valor_retirado": "5000.00",
            "taxa_juros_mensal": "2",
            "quantidade_parcelas": "3",
            "data_contratacao": "2026-09-01",
        },
    )

    resposta = client.get("/emprestimos/1")

    assert resposta.status_code == 200
    conteudo = resposta.get_data(as_text=True)
    assert "#1" in conteudo
    assert "#2" in conteudo
    assert "#3" in conteudo
    assert "Marcar como paga" in conteudo

def test_deve_marcar_parcela_como_paga(client):
    """
    Verifica se marcar uma parcela como paga é refletido no detalhe do empréstimo.
    """

    client.post(
        "/emprestimos/novo",
        data={
            "descricao": "Empréstimo pessoal",
            "valor_retirado": "5000.00",
            "taxa_juros_mensal": "2",
            "quantidade_parcelas": "3",
            "data_contratacao": "2026-09-01"
        },
    )

    resposta = client.post("/emprestimos/1/parcelas/1/pagar")

    assert resposta.status_code == 302

    resposta_detalhe = client.get("/emprestimos/1")

    assert "1/3" in resposta_detalhe.get_data(as_text=True)

def test_detalhe_de_emprestimo_inexistente_nao_deve_quebrar(client):
    """
    Verifica se acessar o detalhe de um id inexistente não derruba a aplicação.
    """

    resposta = client.get("/emprestimos/999")

    assert resposta.status_code == 200
    assert "não encontrado" in resposta.get_data(as_text=True)
