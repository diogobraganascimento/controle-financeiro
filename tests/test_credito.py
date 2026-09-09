"""
Testes do modelo de Crédito.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.models.credito import Credito
from app.models.transacao import Transacao


@pytest.fixture
def credito():
    """
    Cria um crédito válido para utilização nos testes.
    """

    return Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )


def test_deve_criar_credito_valido():
    """
    Verifica se um crédito válido é criado corretamente.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
        comprovante="contracheque.pdf",
    )

    assert credito.descricao == "Salário"
    assert credito.valor == Decimal("5000.00")
    assert credito.data == date(2026, 9, 5)
    assert credito.categoria == "Salário"
    assert credito.comprovante == "contracheque.pdf"


def test_deve_rejeitar_descricao_vazia():
    """
    Verifica se uma descrição vazia gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="A descrição da transação é obrigatória.",
    ):
        Credito(
            descricao="",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_descricao_com_apenas_espacos():
    """
    Verifica se uma descrição contendo apenas espaços
    gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="A descrição da transação é obrigatória.",
    ):
        Credito(
            descricao="   ",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_descricao_que_nao_seja_string():
    """
    Verifica se uma descrição que não seja string
    gera TypeError.
    """

    with pytest.raises(
        TypeError,
        match="A descrição da transação deve ser uma string.",
    ):
        Credito(
            descricao=123,
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_valor_zero():
    """
    Verifica se valor zero gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="O valor da transação deve ser maior que zero.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("0"),
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_valor_negativo():
    """
    Verifica se valor negativo gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="O valor da transação deve ser maior que zero.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("-100"),
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_valor_que_nao_seja_decimal():
    """
    Verifica se valor que não seja Decimal gera TypeError.
    """

    with pytest.raises(
        TypeError,
        match="O valor da transação deve ser um Decimal.",
    ):
        Credito(
            descricao="Salário",
            valor=5000,
            data=date(2026, 9, 5),
            categoria="Salário",
        )


def test_deve_rejeitar_data_que_nao_seja_date():
    """
    Verifica se uma data que não seja date gera TypeError.
    """

    with pytest.raises(
        TypeError,
        match="A data da transação deve ser um objeto date.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data="05/09/2026",
            categoria="Salário",
        )


def test_deve_rejeitar_categoria_vazia():
    """
    Verifica se uma categoria vazia gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="A categoria da transação é obrigatória.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="",
        )


def test_deve_rejeitar_categoria_com_apenas_espacos():
    """
    Verifica se uma categoria contendo apenas espaços
    gera ValueError.
    """

    with pytest.raises(
        ValueError,
        match="A categoria da transação é obrigatória.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria="   ",
        )


def test_deve_rejeitar_categoria_que_nao_seja_string():
    """
    Verifica se uma categoria que não seja string
    gera TypeError.
    """

    with pytest.raises(
        TypeError,
        match="A categoria da transação deve ser uma string.",
    ):
        Credito(
            descricao="Salário",
            valor=Decimal("5000.00"),
            data=date(2026, 9, 5),
            categoria=123,
        )


def test_deve_permitir_comprovante_opcional():
    """
    Verifica se o comprovante pode ser omitido.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )

    assert credito.comprovante is None


def test_deve_permitir_remover_comprovante():
    """
    Verifica se o comprovante pode voltar para None.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
        comprovante="contracheque.pdf",
    )

    credito.comprovante = None

    assert credito.comprovante is None


def test_deve_rejeitar_comprovante_com_tipo_invalido():
    """
    Verifica se comprovante que não seja string ou None
    é rejeitado.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )

    with pytest.raises(
        TypeError,
        match="O comprovante deve ser uma string ou None.",
    ):
        credito.comprovante = 123


def test_deve_remover_espacos_da_descricao_e_categoria():
    """
    Verifica se espaços externos são removidos.
    """

    credito = Credito(
        descricao="   Salário   ",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="   Salário   ",
    )

    assert credito.descricao == "Salário"
    assert credito.categoria == "Salário"


def test_deve_permitir_alterar_valor_valido(credito):
    """
    Verifica se o valor pode ser alterado para um valor válido.
    """

    credito.valor = Decimal("6000.00")

    assert credito.valor == Decimal("6000.00")


def test_nao_deve_permitir_alterar_valor_para_zero(credito):
    """
    Verifica se o valor não pode ser alterado para zero.
    """

    with pytest.raises(
        ValueError,
        match="O valor da transação deve ser maior que zero.",
    ):
        credito.valor = Decimal("0")


def test_nao_deve_permitir_alterar_valor_para_negativo(credito):
    """
    Verifica se o valor não pode ser alterado para número negativo.
    """

    with pytest.raises(
        ValueError,
        match="O valor da transação deve ser maior que zero.",
    ):
        credito.valor = Decimal("-100")


def test_nao_deve_permitir_alterar_descricao_para_vazia(credito):
    """
    Verifica se a descrição não pode ser alterada para vazia.
    """

    with pytest.raises(
        ValueError,
        match="A descrição da transação é obrigatória.",
    ):
        credito.descricao = ""


def test_nao_deve_permitir_alterar_categoria_para_vazia(credito):
    """
    Verifica se a categoria não pode ser alterada para vazia.
    """

    with pytest.raises(
        ValueError,
        match="A categoria da transação é obrigatória.",
    ):
        credito.categoria = ""


def test_nao_deve_permitir_alterar_data_para_string(credito):
    """
    Verifica se a data não pode ser alterada para uma string.
    """

    with pytest.raises(
        TypeError,
        match="A data da transação deve ser um objeto date.",
    ):
        credito.data = "05/09/2026"


def test_credito_deve_ser_uma_transacao(credito):
    """
    Verifica se Credito herda de Transacao.
    """

    assert isinstance(credito, Transacao)

def test_credito_deve_ter_impacto_positivo_no_saldo(credito):
    """
    Verifica se um crédito aumenta o saldo.
    """

    assert credito.impacto_saldo() == Decimal("5000.00")
