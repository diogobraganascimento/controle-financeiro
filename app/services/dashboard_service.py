"""
Serviços de agregação para o dashboard financeiro.

Este módulo concentra os cáclculos de saldo e totais, que são regras de nengócio e por isso não devem ficar dentro das rotas. As somas são feitas pelo próprio banco de dados (função SUM do SQL), em vez de trazer todas as transações para a memória da aplicação e somar em Python.
"""

from decimal import Decimal

from sqlalchemy import func

from app.extensions import db
from app.models.categoria import Categoria as CategoriaModel
from app.models.transacao import Transacao as TransacaoModel
from app.models.emprestimo import Emprestimo as EmprestimoModel
from app.models.parcela import Parcela as ParcelaModel


def _somar_transacoes(tipo: str) -> Decimal:
    """
    Retorna a soma dos valores de todas as transações de um tipo específico (credito ou debito). Retorna 0 se não houver nenhuma transação desse tipo.
    """

    resultado = (
        db.session.query(func.sum(TransacaoModel.valor))
        .filter_by(tipo=tipo)
        .scalar()
    )

    # scalar() retorna None se não houver nenhuma linha somada
    # (nenhuma transação daquele tipo ainda foi cadastrada).
    return resultado if resultado is not None else Decimal("0")

def _somar_parcelas_nao_pagas() -> Decimal:
    """
    Retorna a soma do valor de todas as parcelas de empréstimo ainda não pagas, de todos os empréstimos cadastrados. Retorna 0 se não houver nenhuma parcela em aberto.
    """

    resultado = (
        db.session.query(func.sum(ParcelaModel.valor))
        .filter_by(paga=False)
        .scalar()
    )

    return resultado if resultado is not None else Decimal("0")

def obter_resumo_financeiro() -> dict:
    """
    Retorna um resumo com os indicadores principais do dashboard: total de crédito, total de débitos, saldo atual e quantidade de categorias cadastradas.
    """

    total_creditos = _somar_transacoes("credito")
    total_debitos = _somar_transacoes("debito")

    total_categorias = db.session.query(
        func.count(CategoriaModel.id)
    ).scalar()

    total_emprestimos = db.session.query(
        func.count(EmprestimoModel.id)
    ).scalar()

    valor_comprometido_emprestimos = _somar_parcelas_nao_pagas()

    return {
        "total_creditos": total_creditos,
        "total_debitos": total_debitos,
        "saldo": total_creditos - total_debitos,
        "total_categorias": total_categorias,
        "total_emprestimos": total_emprestimos,
        "valor_comprometido_emprestimos": valor_comprometido_emprestimos,
    }
