"""
Mapeamento entre entidades de domínio e modelos de persistência.
"""

from app.domain.credito import Credito
from app.domain.debito import Debito
from app.domain.transacao import Transacao as TransacaoDomain
from app.extensions import db
from app.models.categoria import Categoria as CategoriaModel
from app.models.transacao import Transacao as TransacaoModel


class CategoriaDaTransacaoNaoEncontradaError(Exception):
    """
    Levantada quando a categoria informada na transação de domínio não está cadastrada com o mesmo nome e o mesmo tipo da transação.
    """

def to_model(transacao: TransacaoDomain) -> TransacaoModel:
    """
    Converte uma transação de domínio em um modelo de persistência.

    A categoria da transação (um texto no domínio) é resolvida para a Categoria já cadastrada com o mesmo nome e o mesmo tipo da transação. Se não existir, a conversão falha - transações não criam categorias novas por conta própria.
    """

    categoria_model = (
        db.session.query(CategoriaModel)
        .filter_by(nome=transacao.categoria, tipo=transacao.tipo)
        .first()
    )
    
    if categoria_model is None:
        raise CategoriaDaTransacaoNaoEncontradaError(
            f"Categoria '{transacao.categoria}' do tipo "
            f"'{transacao.tipo}' não está cadastrada."
        )

    return TransacaoModel(
        tipo=transacao.tipo,
        descricao=transacao.descricao,
        valor=transacao.valor,
        data=transacao.data,
        categoria_id=categoria_model.id,
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
            categoria=transacao.categoria.nome,
            comprovante=transacao.comprovante,
            id=transacao.id,
        )

    if transacao.tipo == "debito":
        return Debito(
            descricao=transacao.descricao,
            valor=transacao.valor,
            data=transacao.data,
            categoria=transacao.categoria.nome,
            comprovante=transacao.comprovante,
            id=transacao.id,
        )

    raise ValueError(
        f"Tipo de transação inválido: {transacao.tipo}"
    )
