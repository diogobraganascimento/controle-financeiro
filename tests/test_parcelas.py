"""
Testes da entidade do domínio Parcelas.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.domain.parcela import Parcela


def test_deve_criar_parcela_valida():
    """
    Verifica se uma parcela válida é criada corretamente, já nascendo como não paga.
    """

    parcela = Parcela(
        numero=1,
        valor=Decimal("450.00"),
        data_vencimento=date(2026, 10, 5),
    )

    assert parcela.numero == 1
    assert parcela.valor == Decimal("450.00")
    assert parcela.data_vencimento == date(2026, 10, 5)
    assert parcela.paga is False

def test_deve_marcar_parcela_como_paga():
    """
    Verifica se o método pagar() marca a parcela como paga.
    """

    parcela = Parcela(
        numero=1,
        valor=Decimal("450.00"),
        data_vencimento=date(2026, 10,5),
    )

    parcela.pagar()

    assert parcela.paga is True

def test_deve_rejeitar_numero_zero_ou_negativo():
    """
    Verifica se um número de parcela inválida é rejeitado.
    """

    with pytest.raises(ValueError):
        Parcela(
            numero=0,
            valor=Decimal("450.00"),
            data_vencimento=date(2026, 10, 5),
        )

def test_deve_rejeitar_valor_zero_ou_negativo():
    """
    Verifica se um valor de parcela inválido é rejeitado.
    """

    with pytest.raises(ValueError):
        Parcela(
            numero=1,
            valor=Decimal("0"),
            data_vencimento=date(2026, 10, 5),
        )
