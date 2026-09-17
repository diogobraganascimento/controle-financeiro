"""
Testes dos mapeamentos entre domínio e persistência.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.domain.credito import Credito
from app.domain.debito import Debito
from app.mappers.transacao_mapper import to_domain
from app.models.categoria import Categoria as CategoriaModel
from app.models.transacao import Transacao as TransacaoModel


def test_deve_converter_modelo_de_credito_para_dominio():
    """
    Verifica se um modelo de persistência de crédito é convertido para a entidade de domínio correta.
    """

    categoria_model = CategoriaModel(nome="Salário", tipo="credito")

    modelo = TransacaoModel(
        tipo="credito",
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria=categoria_model,
        comprovante=None,
    )

    credito = to_domain(modelo)

    assert isinstance(credito, Credito)
    assert credito.tipo == "credito"
    assert credito.descricao == "Salário"
    assert credito.valor == Decimal("5000.00")
    assert credito.categoria == "Salário"

def test_deve_converter_modelo_de_debito_para_domain():
    """
    Verifica se um modelo de persistência de débito é convertido para a entidade de domínio correta.
    """

    categoria_model = CategoriaModel(nome="Moradia", tipo="debito")

    modelo = TransacaoModel(
        tipo="debito",
        descricao="Aluguel",
        valor=Decimal("1800.00"),
        data=date(2026, 9, 10),
        categoria=categoria_model,
        comprovante=None,
    )

    debito = to_domain(modelo)

    assert isinstance(debito, Debito)
    assert debito.tipo == "debito"
    assert debito.descricao == "Aluguel"
    assert debito.valor == Decimal("1800.00")
    assert debito.categoria == "Moradia"

def test_nao_deve_converter_tipo_desconhecido():
    """
    Verifica se um tipo desconhecido gera ValueError.
    """

    categoria_model = CategoriaModel(nome="Teste", tipo="credito")

    modelo = TransacaoModel(
        tipo="banana",
        descricao="Teste",
        valor=Decimal("100.00"),
        data=date(2026, 9, 13),
        categoria=categoria_model,
        comprovante=None
    )

    with pytest.raises(
        ValueError,
        match="Tipo de transação inválido: banana"
    ):
        to_domain(modelo)
