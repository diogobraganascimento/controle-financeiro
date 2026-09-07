""""
Rotas relacionadas à página inicial
"""


from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    """Exibe a página inicial da aplicação."""
    nome_sistema = "Controle Financeiro"

    return render_template(
        "home.html",
        nome_sistema=nome_sistema
    )
