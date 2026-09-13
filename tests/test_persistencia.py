"""
Testes de persistência.
"""

from datetime import date
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

import pytest

from app import create_app
from app.extensions import db
from app.models.transacao import Transacao
from app.domain.credito import Credito
from app.mappers.transacao_mapper import to_model


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

def test_deve_persistir_transacao(app):
    """
    Verifica se uma transação pode ser grava no banco.
    """

    transacao = Transacao(
        tipo="credito",
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
        comprovante=None,
    )

    db.session.add(transacao)
    db.session.commit()

    assert transacao.id is not None

def test_deve_recuperar_transacao_persistida(app):
    """
    Verifica se uma transação pode ser recuperada do banco.
    """

    transacao = Transacao(
        tipo="credito",
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
        comprovante=None,
    )

    db.session.add(transacao)
    db.session.commit()

    transacao_salva = db.session.get(
        Transacao,
        transacao.id,
    )

    assert transacao_salva is not None
    assert transacao_salva.tipo == "credito"
    assert transacao_salva.descricao == "Salário"
    assert transacao_salva.valor == Decimal("5000.00")
    assert transacao_salva.data == date(2026, 9, 5)
    assert transacao_salva.categoria == "Salário"
    assert transacao_salva.comprovante is None

def test_deve_persistir_credito_do_dominio(app):
    """
    Verifica se um Crédito de domínio pode ser convertido e persistido no banco.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )

    modelo = to_model(credito)

    db.session.add(modelo)
    db.session.commit()

    assert modelo.id is not None

    transacao_salva = db.session.get(
        Transacao,
        modelo.id,
    )

    assert transacao_salva is not None

    assert transacao_salva.tipo == "credito"
    assert transacao_salva.descricao == "Salário"
    assert transacao_salva.valor == Decimal("5000.00")

def test_nao_deve_persistir_tipo_invalido(app):
    """
    Verifica se o banco rejeita um tipo de transação inválida.
    """

    transacao = Transacao(
        tipo="banana",
        descricao="Teste",
        valor=Decimal("1000.00"),
        data=date(2026, 9, 13),
        categoria="Teste"
    )

    db.session.add(transacao)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()
