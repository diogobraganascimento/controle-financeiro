""""
Rotas relacionadas à página inicial
"""


from flask import Blueprint, render_template

from app.services.dashboard_service import obter_resumo_financeiro

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    """Exibe o dashboard financeiro na página inicial."""

    nome_sistema = "Controle Financeiro"
    resumo = obter_resumo_financeiro()

    # Dados dos gráficos, já convertidos para float (JSON não
    # entende Decimal), separados do "resumo" exibido em texto.
    grafico = {
        "composicao": {
            "creditos": float(resumo["total_creditos"]),
            "debitos": float(resumo["total_debitos"]),
        },
        "evolucao": {
            "labels": [item["label"] for item in resumo["evolucao_mensal"]],
            "valores": [float(item["saldo"]) for item in resumo["evolucao_mensal"]],
        },
    }

    return render_template(
        "home.html",
        nome_sistema=nome_sistema,
        resumo=resumo,
        grafico=grafico,
    )
