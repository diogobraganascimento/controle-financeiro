"""
Testes do serviço de relatórios financeiros.
"""

from datetime import date
from decimal import Decimal

import pytest

from app import create_app
from app.domain.categoria import Categoria as CategoriaDomain
from app.domain.credito import Credito
from app.domain.debito import Debito
from app.extensions import db
from app.mappers.categoria_mapper import to_model as categoria_to_model
from app.mappers.transacao_mapper import to_model as transacao_to_model
from app.services.relatorio_service import relatorio_anual, relatorio_mensal


@pytest.fixture
def app():
    """
    Cria uma aplicação Flask configurada para testes, com duas
    categorias e transações em meses e anos diferentes, para
    verificar se os relatórios filtram corretamente por período.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

        categoria_salario = categoria_to_model(
            CategoriaDomain(nome="Salário", tipo="credito")
        )
        categoria_moradia = categoria_to_model(
            CategoriaDomain(nome="Moradia", tipo="debito")
        )
        db.session.add(categoria_salario)
        db.session.add(categoria_moradia)
        db.session.commit()

        # Setembro de 2026: R$ 5000 de crédito, R$ 1800 de débito.
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

        # Outubro de 2026: R$ 5000 de crédito.
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

        # Setembro de 2025 (ano deferente): não deve aparecer nos
        # relatórios de 2026
        db.session.add(
            transacao_to_model(
                Credito(
                    descricao="Salário antigo",
                    valor=Decimal("4000.00"),
                    data=date(2025, 9, 5),
                    categoria="Salário",
                )
            )
        )

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

def test_relatorio_mensal_deve_filtrar_apenas_o_mes_pedido(app):
    """
    Verifica se o relatório mensal considera apenas as
    transações do mês e ano informados.
    """

    relatorio = relatorio_mensal(ano=2026, mes=9)

    assert relatorio["total_creditos"] == Decimal("5000.00")
    assert relatorio["total_debitos"] == Decimal("1800.00")
    assert relatorio["saldo"] == Decimal("3200.00")

def test_relatorio_mensal_deve_agrupar_por_categoria(app):
    """
    Verifica se o relatório mensal agrupa corretamente os
    valores por categoria.
    """

    relatorio = relatorio_mensal(ano=2026, mes=9)

    assert relatorio["creditos_por_categoria"] == [
        {"categoria": "Salário", "total": Decimal("5000.00")}
    ]
    assert relatorio["debitos_por_categoria"] == [
        {"categoria": "Moradia", "total": Decimal("1800.00")}
    ]

def test_relatorio_mensal_sem_transacao_deve_ser_zero(app):
    """
    Verifica se um mês sem nenhuma transação retorna totais
    zerados, sem quebrar.
    """

    relatorio = relatorio_mensal(ano=2026, mes=1)

    assert relatorio["total_creditos"] == Decimal("0")
    assert relatorio["total_debitos"] == Decimal("0")
    assert relatorio["creditos_por_categoria"] == []

def test_relatorio_anual_deve_somar_todos_os_meses_do_ano(app):
    """
    Verifica se o relatório anual soma corretamente as
    transações de setembro e outubro de 2026, ignorando 2025.
    """

    relatorio = relatorio_anual(ano=2026)

    assert relatorio["total_creditos"] == Decimal("10000.00")
    assert relatorio["total_debitos"] == Decimal("1800.00")
    assert relatorio["saldo"] == Decimal("8200.00")

def test_relatorio_anual_deve_distribuir_totais_por_mes(app):
    """
    Verifcia se o relatório anual posiciona corretamente os valores de cada mês na lista de 12 posições.
    """

    relatorio = relatorio_anual(ano=2026)

    # Índice 8 = setembro (mês 9, lista começa em janeiro = índice 0).
    assert relatorio["creditos_mensais"][8] == Decimal("5000.00")
    # Índice 9 = outubro
    assert relatorio["creditos_mensais"][9] == Decimal("5000.00")
    # Índice 0 = Janeiro, sem nenhuma transação
    assert relatorio["creditos_mensais"][0] == Decimal("0")
