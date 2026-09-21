"""
Testes da entidade de domínio Emprestimo.
"""

from datetime import date
from decimal import Decimal

import pytest

from app.domain.emprestimo import Emprestimo


def test_deve_calcular_valor_da_parcela_pelo_sistema_price():
    """
    Verifica se o valor da parcela é calculada corretamente pela fórmula do Sistema Price.
    
    Exemplo conferido manualmente: R$ 5.000,00 emprestados a 2% ao mês, em 12 parcelas, resulta em parcelas de aprocimadamente R$ 472,84.
    """

    emprestimo = Emprestimo(
        descricao="Emprestimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=12,
        data_contratacao=date(2026, 9, 1),
    )

    assert emprestimo.valor_parcela == Decimal("472.80")

def test_deve_gerar_a_quantidade_correta_de_parcelas():
    """
    Verifica se o empréstimo gera uma parcela para cada mês contratado, com vencimento mensal a partir da contratação.
    """

    emprestimo = Emprestimo(
        descricao="Emprestimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    assert len(emprestimo.parcelas) == 3
    assert emprestimo.parcelas[0].data_vencimento == date(2026, 10, 1)
    assert emprestimo.parcelas[1].data_vencimento == date(2026, 11, 1)
    assert emprestimo.parcelas[2].data_vencimento == date(2026, 12, 1)

def test_valor_final_deve_ser_parcela_vezes_quantidade():
    """
    Verifica se o valor final é a soma de todas as parcelas.
    """

    emprestimo = Emprestimo(
        descricao="Emprestimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=12,
        data_contratacao=date(2026, 9, 1),
    )

    assert emprestimo.valor_final == emprestimo.valor_parcela * 12

def test_situacao_deve_ser_ativo_com_parcelas_nao_pagas():
    """
    Verifica se a situação e "ativo" enquanto houver parcelas não pagas.
    """

    emprestimo = Emprestimo(
        descricao="Emprestimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    assert emprestimo.situacao == "ativo"
    assert emprestimo.parcelas_pagas == 0
    assert emprestimo.parcelas_restantes == 3

def test_situacao_deve_ser_quitado_com_todas_as_parcelas_pagas():
    """
    VErifica se a situação nuda para "quitado" quando todas as parcelas são marcadas como pagas.
    """

    emprestimo = Emprestimo(
        descricao="Emprestimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=2,
        data_contratacao=date(2026, 9, 1),
    )

    for parcela in emprestimo.parcelas:
        parcela.pagar()

    assert emprestimo.situacao == "quitado"
    assert emprestimo.parcelas_restantes == 0
    assert emprestimo.valor_restante == Decimal("0")

def test_deve_rejeitar_taxa_de_juros_zero():
    """
    Verifica se uma taxa de kjurows zero é rejeitada, já que a fórmula do Sistema Price não é aplicável. nesse caso.
    """

    with pytest.raises(ValueError):
        emprestimo = Emprestimo(
            descricao="Emprestimo sem juros",
            valor_retirado=Decimal("5000.00"),
            taxa_juros_mensal=Decimal("0"),
            quantidade_parcelas=12,
            data_contratacao=date(2026, 9, 1),
        )

def test_deve_rejeitar_valor_retirado_zero_ou_negativo():
    """
    Verifica se um valor retirado inválido é rejeitado.
    """

    with pytest.raises(ValueError):
        emprestimo = Emprestimo(
            descricao="Emprestimo pessoal",
            valor_retirado=Decimal("0"),
            taxa_juros_mensal=Decimal("0.02"),
            quantidade_parcelas=12,
            data_contratacao=date(2026, 9, 1),
        )
