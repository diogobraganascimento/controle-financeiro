"""
Teste do comportamento comum de transações.
"""

from datetime import date
from decimal import Decimal

from app.models.credito import Credito
from app.models.debito import Debito


def test_lista_de_transacoes_deve_calcular_saldo():
    """
    Verifica se diferentes tipos de transação podem ser processados através da mesma interface.
    """

    transacoes = [
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="Salário",
        ),
        Debito(
            descricao="Aluguel",
            valor=Decimal("1800.00"),
            data=date(2026, 9, 10),
            categoria="Moradia",
        ),
    ]

    saldo = sum(
        transacao.impacto_saldo()
        for transacao in transacoes
    )

    assert saldo == Decimal("3200.00")
