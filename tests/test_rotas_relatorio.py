"""
Testes das rotas HTTP de relatórios financeiros.
"""

from datetime import date
from decimal import Decimal

import pytest

from app import create_app
from app.domain.categoria import Categoria as CategoriaDomain
from app.domain.credito import Credito
from app.extensions import db
from app.mappers.categoria_mapper import to_model as categoria_to_model
from app.mappers.transacao_mapper import to_model as transacao_to_model


@pytest.fixture
def client():
    """
    Cria um cliente de teste Flask com banco em memória e uma
    transação já cadastrada.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

        categoria = categoria_to_model(
            CategoriaDomain(nome="Salário", tipo="credito")
        )
        db.session.add(categoria)
        db.session.commit()

        db.session.add(
            transacao_to_model(
                Credito(
                    descricao="Salário",
                    valor=Decimal("5000.00"),
                    data=date(2026, 9, 5),
                    categoria="Salário",
                )
            )
        )
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()

def test_deve_exibir_pagina_inicial_de_relatorio(client):
    """
    Verifica se a página inicial de relatórios responde
    corretamente.
    """

    resposta = client.get("/relatorios/")

    assert resposta.status_code == 200
    assert "Relatório Mensal" in resposta.get_data(as_text=True)

def test_deve_exibir_relatorio_mensal_com_periodo_informado(client):
    """
    Verifica se o relatório mensal exibe os dados do período
    passado via parâmetros de URL.
    """

    resposta = client.get("/relatorios/mensal?ano=2026&mes=9")

    assert resposta.status_code == 200
    conteudo = resposta.get_data(as_text=True)
    assert "Setembro de 2026" in conteudo
    assert "5000.00" in conteudo

def test_deve_exibir_relatorio_anual_com_ano_informado(client):
    """
    Verifica se o relatório anual exibe os dados do ano passado
    via parâmetro de URL.
    """

    resposta = client.get("/relatorios/anual?ano=2026")

    assert resposta.status_code == 200
    conteudo = resposta.get_data(as_text=True)
    assert "Relatório Anual de 2026" in conteudo
    assert "5000.00" in conteudo
