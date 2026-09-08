"""
Testes do modelo de Débito.
"""

from datetime import date
from decimal import Decimal

from app.models.debito import Debito
from app.models.transacao import Transacao


def test_debito_deve_ser_uma_transacao():
    """
    Verifica se Debito herda de Transacao.
    """

    debito = Debito(
        descricao="Aluguel",
        valor=Decimal("1800.00"),
        data=date(2026, 9, 10),
        categoria="Moradia",
    )

    assert isinstance(debito, Transacao)
