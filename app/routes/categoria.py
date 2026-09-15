"""
Rotas para gereinciamento de Categorias.
"""

from flask import Blueprint, redirect, render_template, request, url_for

from app.services.categoria_service import (
    CategoriaJaExisteError,
    criar_categoria,
    listar_categorias,
)


categoria_bp = Blueprint(
    "categoria",
    __name__,
    url_prefix="/categorias",
)

@categoria_bp.route("/", methods=["GET"])
def listar():
    """
    Exibe a lista de categorias cadastradas.
    """

    categorias = listar_categorias()

    return render_template(
        "categorias/listar.html",
        categorias=categorias,
    )

@categoria_bp.route("/nova", methods=["GET", "POST"])
def nova():
    """
    Exibe o formulário de cadastro (GET) e processa o cadastro de uma nova categoria (POST).
    """

    if request.method == "POST":
        nome = request.form.get("nome", "")
        tipo = request.form.get("tipo", "")

        try:
            criar_categoria(nome=nome, tipo=tipo)
        except (ValueError, TypeError, CategoriaJaExisteError) as erro:
            return render_template(
                "categorias/nova.html",
                erro=str(erro),
                nome=nome,
                tipo=tipo,
            )

        return redirect(url_for("categoria.listar"))

    return render_template(
        "categorias/nova.html",
        nome="",
        tipo="",
    )
