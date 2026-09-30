"""
Serviço de agregação para relatórios financeiros mensais e anuais.

Assim como o dashboard, os relatórios não introduzem nenhuma
entidade de domínio nova: são consultas agregadas sobre Transacao
e Categoria, feitas pelo próprio banco de dados.
"""

from decimal import Decimal

from sqlalchemy import extract, func

from app.extensions import db
from app.models.categoria import Categoria as CategoriaModel
from app.models.transacao import Transacao as TransacaoModel


def _totais_por_categoria(tipo: str, ano: int, mes: int | None = None) -> list[dict]:
    """
    Retorna o total de transação de um tipo, agrupapo por categoria, dentro de um ano (e opcionalmente um mês específico).
    Categorias sem nenhuma transação no periodo não aparecem no resultado.
    """

    consulta = (
        db.session.query(
            CategoriaModel.nome,
            func.sum(TransacaoModel.valor),
        )
        .join(
            TransacaoModel,
            TransacaoModel.categoria_id == CategoriaModel.id,
        )
        .filter(TransacaoModel.tipo == tipo)
        .filter(extract("year", TransacaoModel.data) == ano)
    )

    if mes is not None:
        consulta = consulta.filter(
            extract("month", TransacaoModel.data) == mes
        )

    consulta = consulta.group_by(CategoriaModel.nome).order_by(
        CategoriaModel.nome
    )

    return [
        {"categoria": nome, "total": total}
        for nome, total in consulta.all()
    ]

def relatorio_mensal(ano: int, mes: int) -> dict:
    """
    Retorna o relatório financeiro de um mês específico: totais
    de créditos e débitos, saldo, e o detalhamento por categoria.
    """

    creditos_por_categoria = _totais_por_categoria("credito", ano, mes)
    debitos_por_categoria = _totais_por_categoria("debito", ano, mes)

    total_creditos = sum(
        (item["total"] for item in creditos_por_categoria),
        start=Decimal("0"),
    )
    total_debitos = sum(
        (item["total"] for item in debitos_por_categoria),
        start=Decimal("0")
    )

    return {
        "ano": ano,
        "mes": mes,
        "total_creditos": total_creditos,
        "total_debitos": total_debitos,
        "saldo": total_creditos - total_debitos,
        "creditos_por_categoria": creditos_por_categoria,
        "debitos_por_categoria": debitos_por_categoria,
    }

def _totais_mensais_do_ano(tipo: str, ano: int) -> list[Decimal]:
    """
    Retorna uma lista com 12 posições (uma por mês, de janeiro a
    dezembro), cada uma com o total de transações daquele tipo
    naquele mês. Meses sem nenhuma transação aparecem como 0.
    """

    consulta = (
        db.session.query(
            extract("month", TransacaoModel.data),
            func.sum(TransacaoModel.valor),
        )
        .filter(TransacaoModel.tipo == tipo)
        .filter(extract("year", TransacaoModel.data) == ano)
        .group_by(extract("month", TransacaoModel.data))
    )

    totais_por_mes = {int(mes): total for mes, total in consulta.all()}

    return [totais_por_mes.get(mes, Decimal("0")) for mes in range(1, 13)]

def relatorio_anual(ano: int) -> dict:
    """
    Retorna o relatório financeiro de um ano inteiro: totais
    mês a mês de créditos, débitos e saldo, além do detalhamento
    por categoria do ano inteiro.
    """

    creditos_mensais = _totais_mensais_do_ano("credito", ano)
    debitos_mensais = _totais_mensais_do_ano("debito", ano)
    saldos_mensais = [
        credito - debito
        for credito, debito in zip(creditos_mensais, debitos_mensais)
    ]

    total_creditos = sum(creditos_mensais, start=Decimal("0"))
    total_debitos = sum(debitos_mensais, start=Decimal("0"))

    return {
        "ano": ano,
        "creditos_mensais": creditos_mensais,
        "debitos_mensais": debitos_mensais,
        "saldos_mensais": saldos_mensais,
        "total_creditos": total_creditos,
        "total_debitos": total_debitos,
        "saldo": total_creditos - total_debitos,
        "creditos_por_categoria": _totais_por_categoria("credito", ano),
        "debitos_por_categoria": _totais_por_categoria("debito", ano),
    }
