"""
Serviços de aplicação para Crédito e Débito.

Este módulo orquestra a criação e consulta de transações, conectando o domínio, o mapper e a persistência. A criação é polimórfica: quem chama este serviço decide se quer um Credito ou um Debito, passando a classe correspondente.
"""

from app.domain.transacao import Transacao as TransacaoDomain
from app.extensions import db
from app.mappers.transacao_mapper import to_domain, to_model
from app.models.categoria import Categoria as CategoriaModel
from app.models.transacao import Transacao as TransacaoModel


class TransacaoNaoEncontradaError(Exception):
    """
    Levantada quando nenhuma transação é encontrada com o id informado.
    """

def listar_transacoes(tipo: str) -> list[TransacaoDomain]:
    """
    Retorna as transações de um tipo específico (credito ou debito), da mais recente para a mais antiga, já convertidas para entidades de domínio.
    """

    modelos = (
        db.session.query(TransacaoModel)
        .filter_by(tipo=tipo)
        .order_by(TransacaoModel.data.desc())
        .all()
    )

    return [to_domain(modelo) for modelo in modelos]

def obter_transacao(transacao_id: int) -> TransacaoDomain:
    """
    Busca uma transação pelo id.
    
    Levanta TransacaoNaoEncontradaError se não exitir nenhuma transação com esse id.
    """

    modelo = db.session.get(TransacaoModel, transacao_id)

    if modelo is None:
        raise TransacaoNaoEncontradaError(
            f"Transação com id {transacao_id} não encontrada."
        )

    return to_domain(modelo)

def criar_transacao(
        classe,
        descricao: str,
        valor,
        data,
        categoria: str,
        comprovante: str | None = None,
) -> TransacaoDomain:
    """
    Cria e persiste uma nova transação.
    
    `classe` é Credito ou Debito. A validação de negócio (valor positivo, descrição obrigatória etc.) acontece no construtor da classe de domínio. Se a categoria informada não estiver cadastrada, o mapper levanta CategoriaDaTransacaoNaoEncontradaError.
    """

    transacao = classe(
        descricao=descricao,
        valor=valor,
        data=data,
        categoria=categoria,
        comprovante=comprovante,
    )

    modelo = to_model(transacao)

    db.session.add(modelo)
    db.session.commit()

    return to_domain(modelo)

def atualizar_transacao(
        transacao_id: int,
        classe,
        descricao: str,
        valor,
        data,
        categoria: str,
        comprovante: str | None = None,
) -> TransacaoDomain:
    """
    Atualiza uma transação existente.
    
    Levanta TransacaoNaoEncontradaError se o id não existir. A validação de negócio acontece coonstruindo uma entidade de comínio temporária com os novos dados, antes de aplicá-los ao modelo - assim reaproveitando as mesmas regras usadas na criação.
    """

    modelo = db.session.get(TransacaoModel, transacao_id)

    if modelo is None:
        raise TransacaoNaoEncontradaError(
            f"Transação com id {transacao_id} não encontrada."
        )

    # Reaproveitando as validações de dominio antes de alterar o modelo.
    transacao_validada = classe(
        descricao=descricao,
        valor=valor,
        data=data,
        categoria=categoria,
        comprovante=comprovante,
    )

    categoria_model = (
        db.session.query(CategoriaModel)
        .filter_by(nome=transacao_validada.categoria, tipo=modelo.tipo)
        .first()
    )

    if categoria_model is None:
        from app.mappers.transacao_mapper import (
            CategoriaDaTransacaoNaoEncontradaError,
        )

        raise CategoriaDaTransacaoNaoEncontradaError(
            f"Categoria '{transacao_validada.categoria}' do tipo "
            f"'{modelo.tipo}' não está cadastrada."
        )

    modelo.descricao = transacao_validada.descricao
    modelo.valor = transacao_validada.valor
    modelo.data = transacao_validada.data
    modelo.categoria_id = categoria_model.id
    modelo.comprovante = transacao_validada.comprovante

    db.session.commit()

    return to_domain(modelo)

def excluir_transacao(transacao_id: int) -> None:
    """
    Remove uma transação pelo id.
    
    Levanta TransacaoNaoEncontradaError se o id não existir.
    """

    modelo = db.session.get(TransacaoModel, transacao_id)

    if modelo is None:
        raise TransacaoNaoEncontradaError(
            f"Transação com id {transacao_id} não encontrada."
        )

    db.session.delete(modelo)
    db.session.commit()
