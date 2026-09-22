"""
Mapeamento entre entidade de domínio e modelos de persitência para empréstimo.
"""

from app.domain.emprestimo import Emprestimo as EmprestimoDomain
from app.domain.parcela import Parcela as ParcelaDomain
from app.models.emprestimo import Emprestimo as EmprestimoModel
from app.models.parcela import Parcela as ParcelaModel


def to_model(emprestimo: EmprestimoDomain) -> EmprestimoModel:
    """
    Converte um empréstimo de domínio (com suas parcelas) em um modelo de persistência.
    """

    modelo = EmprestimoModel(
        descricao=emprestimo.descricao,
        valor_retirado=emprestimo.valor_retirado,
        taxa_juros_mensal=emprestimo.taxa_juros_mensal,
        quantidade_parcelas=emprestimo.quantidade_parcelas,
        data_contratacao=emprestimo.data_contratacao,
        valor_parcela=emprestimo.valor_parcela,
    )

    modelo.parcelas = [
        ParcelaModel(
            numero=parcela.numero,
            valor=parcela.valor,
            data_vencimento=parcela.data_vencimento,
            paga=parcela.paga,
        )
        for parcela in emprestimo.parcelas
    ]

    return modelo

def to_domain(emprestimo: EmprestimoModel) -> EmprestimoDomain:
    """
    Converte um modelo de persistência em uma entidade de domínio, preservando o estado real das parcelas (inclusive quais já foram pagas).
    """

    parcelas = [
        ParcelaDomain(
            numero=parcela.numero,
            valor=parcela.valor,
            data_vencimento=parcela.data_vencimento,
            paga=parcela.paga,
            id=parcela.id,
        )
        for parcela in emprestimo.parcelas
    ]

    return EmprestimoDomain(
        descricao=emprestimo.descricao,
        valor_retirado=emprestimo.valor_retirado,
        taxa_juros_mensal=emprestimo.taxa_juros_mensal,
        quantidade_parcelas=emprestimo.quantidade_parcelas,
        data_contratacao=emprestimo.data_contratacao,
        parcelas=parcelas,
        valor_parcela=emprestimo.valor_parcela,
        id=emprestimo.id,
    )
