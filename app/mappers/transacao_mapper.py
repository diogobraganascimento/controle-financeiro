"""
Mapeamento entre entidades de domínio e modelos de persistência.
"""

from app.domain.credito import Credito
from app.domain.debito import Debito
from app.domain.transacao import Transacao as TransacaoDomain
from app.models.transacao import Transacao as TransacaoModel


def to_model(transacao: TransacaoDomain) -> TransacaoModel:
    """
    Converte uma transação de domínio em um modelo de persistência.
    """

    return TransacaoModel(
        tipo=transacao.tipo,
        descricao=transacao.descricao,
        valor=transacao.valor,
        data=transacao.data,
        categoria=transacao.categoria,
        comprovante=transacao.comprovante,
    )

def to_domain(transacao: TransacaoModel) -> TransacaoDomain:
    """
    Converte um modelo de persistência em uma entidade de domínio.
    """

    if transacao.tipo == "credito":
        return Credito(
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data,
            categoria=transacao.categoria,
            comprovante=transacao.comprovante,
        )

    if transacao.tipo == "debito":
        return Debito(
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data,
            categoria=transacao.categoria,
            comprovante=transacao.comprovante,
        )

    raise ValueError(
        f"Tipo de transação inválido: {transacao.tipo}"
    )
