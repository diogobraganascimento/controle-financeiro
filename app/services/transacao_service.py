"""
Serviços de aplicação para Crédito e Débito.

Este módulo orquestra a criação e consulta de transações, conectando o domínio, o mapper e a persistência. A criação é polimórfica: quem chama este serviço decide se quer um Credito ou um Debito, passando a classe correspondente.
"""

from app.domain.transacao import Transacao as TransacaoDomain
from app.extensions import db
from app.mappers.transacao_mapper import to_domain, to_model
from app.models.transacao import Transacao as TransacaoModel


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
