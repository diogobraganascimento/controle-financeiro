"""
Testes dos mapeamentos entre domínio e persistência para empréstimos.
"""

from datetime import date
from decimal import Decimal

from app.domain.emprestimo import Emprestimo as EmprestimoDomain
from app.mappers.emprestimo_mapper import to_domain, to_model


def test_deve_converter_emprestimo_para_modelo_de_persistencia():
    """
    Verifica se um empréstimo de domínio, com suas parcelas, é convertido corretamente para o modelo SQLAlchemy.
    """

    emprestimo = EmprestimoDomain(
        descricao="Empréstimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    modelo = to_model(emprestimo)

    assert modelo.descricao == "Empréstimo pessoal"
    assert modelo.valor_retirado == Decimal("5000.00")
    assert modelo.valor_parcela == emprestimo.valor_parcela
    assert len(modelo.parcelas) == 3
    assert modelo.parcelas[0].numero == 1
    assert modelo.parcelas[0].paga is False

def test_deve_converter_modelo_de_emprestimo_para_dominio_preservando_parcelas_pagas():
    """
    Verifica se, ao converter de volta para o domínio, o estado de cada parcela (paga ou não) é preservado.
    """

    emprestimo = EmprestimoDomain(
        descricao="Empréstimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    modelo = to_model(emprestimo)
    modelo.parcelas[0].paga = True

    emprestimo_reconstruido = to_domain(modelo)

    assert emprestimo_reconstruido.parcelas[0].paga is True
    assert emprestimo_reconstruido.parcelas[1].paga is False
    assert emprestimo_reconstruido.parcelas_pagas == 1
    assert emprestimo_reconstruido.valor_parcela == emprestimo.valor_parcela

