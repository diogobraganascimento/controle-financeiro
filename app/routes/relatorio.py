"""
Rotas para relatórios financeiros mensais e anuais.
"""

from datetime import date

from flask import Blueprint, render_template, request

from app.services.relatorio_service import relatorio_anual, relatorio_mensal


relatorio_bp = Blueprint(
    "relatorio",
    __name__,
    url_prefix="/relatorios",
)

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

@relatorio_bp.route("/", methods=["GET"])
def index():
    """
    Exibe a página inicial de relatórios, com formulários para
    escolher o relatório mensal ou anual.
    """

    hoje = date.today()

    return render_template(
        "relatorios/index.html",
        ano_atual=hoje.year,
        mes_atual=hoje.month,
        meses=MESES,
    )

@relatorio_bp.route("/mensal", methods=["GET"])
def mensal():
    """
    Exibe o relatório financeiro de um mês específico.

    O ano e o mês vêm como parâmetros de URL (?ano=2026&mes=9);
    se não informados, usa o mês atual.
    """

    hoje = date.today()
    ano = request.args.get("ano", type=int, default=hoje.year)
    mes = request.args.get("mes", type=int, default=hoje.month)

    relatorio = relatorio_mensal(ano, mes)

    return render_template(
        "relatorios/mensal.html",
        relatorio=relatorio,
        nome_mes=MESES[mes - 1],
    )

@relatorio_bp.route("anual", methods=["GET"])
def anual():
    """
    Exibe o relatório financeiro de um ano inteiro.

    O ano vem como parâmetro de URL (?ano=2026); se não
    informado, usa o ano atual.
    """

    hoje = date.today()
    ano = request.args.get("ano", type=int, default=hoje.year)

    relatorio = relatorio_anual(ano)

    return render_template(
        "relatorios/anual.html",
        relatorio=relatorio,
        meses=MESES,
    )

