"""
Teste do serviço e da reta de dashboard financeiro.
"""

from datetime import date
from decimal import Decimal

import pytest

from app import create_app
from app.extensions import db
from app.services.dashboard_service import obter_resumo_financeiro
from app.services.dashboard_service import obter_evolucao_mensal
from app.domain.categoria import Categoria as CategoriaDomain
from app.domain.credito import Credito
from app.domain.debito import Debito
from app.mappers.categoria_mapper import to_model as categoria_to_model
from app.mappers.transacao_mapper import to_model as transacao_to_model
from app.services.dashboard_service import obter_evolucao_mensal


@pytest.fixture
def app():
    """
    Cria uma aplicação Flask configurada para testes.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

def test_resumo_deve_ser_zero_sem_nenhum_transacao(app):
    """
    Verifica se o resumo financeiro é zero quando não há nenhuma transação nem categoria cadastrada.
    """

    resumo = obter_resumo_financeiro()

    assert resumo["total_creditos"] == Decimal("0")
    assert resumo["total_debitos"] == Decimal("0")
    assert resumo["saldo"] == Decimal("0")
    assert resumo["total_categorias"] == 0

def test_resumo_deve_calcular_saldo_corretamente(app):
    """
    Verifica se o saldo é calculado corretamente a partir de crédito e débitos cadastrados.
    """

    from app.domain.credito import Credito
    from app.domain.debito import Debito
    from app.mappers.categoria_mapper import to_model as categoria_to_model
    from app.mappers.transacao_mapper import to_model as transacao_to_model
    from app.domain.categoria import Categoria as CategoriaDomain


    categoria_credito = categoria_to_model(
        CategoriaDomain(nome="Salário", tipo="credito")
    )
    categoria_debito = categoria_to_model(
        CategoriaDomain(nome="Moradia", tipo="debito")
    )

    db.session.add(categoria_credito)
    db.session.add(categoria_debito)
    db.session.commit()

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )
    debito = Debito(
        descricao="Alugiel",
        valor=Decimal("1800.00"),
        data=date(2026, 9, 10),
        categoria="Moradia",
    )

    db.session.add(transacao_to_model(credito))
    db.session.add(transacao_to_model(debito))
    db.session.commit()

    resumo = obter_resumo_financeiro()

    assert resumo["total_creditos"] == Decimal("5000.00")
    assert resumo["total_debitos"] == Decimal("1800.00")
    assert resumo["saldo"] == Decimal("3200.00")
    assert resumo["total_categorias"] == 2

def test_pagina_inicial_deve_exibir_o_resumo(app):
    """
    Verifica se a página inicial redenriza o resumo financeiro corretamente.
    """

    with app.test_client() as client:
        resposta = client.get("/")

        assert resposta.status_code == 200
        assert "Resumo Financeiro" in resposta.get_data(as_text=True)
        assert "Saldo atual" in resposta.get_data(as_text=True)

def test_resumo_considerar_valor_comprometido_com_emprestimo(app):
    """
    Verifica se o resumo financeiro soma corretamente o valor das parcelas de empréstimo ainda não pagas.
    """

    from app.domain.emprestimo import Emprestimo as EmprestimoDomain
    from app.mappers.emprestimo_mapper import to_model as emprestimo_to_model

    emprestimo = EmprestimoDomain(
        descricao="Empréstimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    modelo = emprestimo_to_model(emprestimo)

    db.session.add(modelo)
    db.session.commit()

    # Marca a primeira parcela como paga, para confirmar que ela não entra na soma do valor comprometido.
    modelo.parcelas[0].paga = True
    db.session.commit()

    resumo = obter_resumo_financeiro()

    valor_esperado = emprestimo.valor_parcela * 2 # 2 parcelas em aberto

    assert resumo["total_emprestimos"] == 1
    assert resumo["valor_comprometido_emprestimos"] == valor_esperado

def test_evolucao_mensal_deve_ter_o_tamanho_pedido(app):
    """
    Verifica se a evolução mensal retorna a quantidade de meses
    solicitada, com os rótulos corretos.
    """

    evolucao = obter_evolucao_mensal(meses=6, data_referencia=date(2026, 10, 15))

    assert len(evolucao) == 6
    assert evolucao[0]["label"] == "Mai/2026"
    assert evolucao[-1]["label"] == "Out/2026"

def test_evolucao_mensal_deve_distribuir_saldo_por_mes(app):
    """
    Verifica se a evolução mensal calcula corretamente o saldo
    de cada mês, inclusive meses sem nenhuma transação.
    """

    categoria_credito = categoria_to_model(
        CategoriaDomain(nome="Salário", tipo="credito")
    )
    categoria_debito = categoria_to_model(
        CategoriaDomain(nome="Moradia", tipo="debito")
    )
    db.session.add(categoria_credito)
    db.session.add(categoria_debito)
    db.session.commit()

    db.session.add(
        transacao_to_model(
            Credito(
                descricao="Salário",
                valor=Decimal("5000.00"),
                data=date(2026, 9, 5),
                categoria="Salário"
            )
        )
    )
    db.session.add(
        transacao_to_model(
            Debito(
                descricao="Aluguel",
                valor=Decimal("1800.00"),
                data=date(2026, 9, 10),
                categoria="Moradia",
            )
        )
    )
    db.session.add(
    transacao_to_model(
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data=date(2026, 10, 5),
            categoria="Salário",
        )    
    )
    )
    db.session.commit()

    evolucao = obter_evolucao_mensal(meses=3, data_referencia=date(2026, 10, 15))

    assert len(evolucao) == 3
    assert evolucao[0]["label"] == "Ago/2026"
    assert evolucao[0]["saldo"] == Decimal("0")
    assert evolucao[1]["label"] == "Set/2026"
    assert evolucao[1]["saldo"] == Decimal("3200.00")
    assert evolucao[2]["label"] == "Out/2026"
    assert evolucao[2]["saldo"] == Decimal("5000.00")

def test_pagina_inicial_deve_incluir_graficos(app):
    """
    Verifica se a página inicial carrega o Chart.js e os
    elementos canvas dos gráficos.
    """

    with app.test_client() as client:
        resposta = client.get("/")

        conteudo = resposta.get_data(as_text=True)
        assert "graficoComposicao" in conteudo
        assert "graficoEvolucao" in conteudo
        assert "Chart.js" in conteudo or "chart.umd" in conteudo
