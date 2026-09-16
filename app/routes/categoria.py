"""
Rotas para gereinciamento de Categorias.
"""

from flask import Blueprint, redirect, render_template, request, url_for

from app.services.categoria_service import (
    CategoriaJaExisteError,
    CategoriaNaoEncontradaError,
    atualizar_categoria,
    criar_categoria,
    excluir_categoria,
    listar_categorias,
    obter_categoria,
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
        erro=None,
        nome="",
        tipo="",
    )

@categoria_bp.route("/<int:categoria_id>/editar", methods=["GET", "POST"])
def editar(categoria_id):
    """
    Exibe o formulário de edição (GET) e processa a atualização de uma categoria existente (POST).
    """

    try:
        categoria_atual = obter_categoria(categoria_id)
    except CategoriaNaoEncontradaError as erro:
        return render_template(
            "categorias/listar.html",
            categorias=listar_categorias(),
            erro=str(erro)
        )

    if request.method == "POST":
        nome = request.form.get("nome", "")
        tipo = request.form.get("tipo", "")

        try:
            atualizar_categoria(
                categoria_id=categoria_id,
                nome=nome,
                tipo=tipo,
            )
        except (ValueError, TypeError, CategoriaJaExisteError) as erro:
            return render_template(
                "categoria/editar.html",
                erro=str(erro),
                categoria_id=categoria_id,
                nome=nome,
                tipo=tipo,
            )

        return redirect(url_for("categoria.listar"))

    return render_template(
        "categorias/editar.html",
        erro=None,
        categoria_id=categoria_id,
        nome=categoria_atual.nome,
        tipo=categoria_atual.tipo,
    )

@categoria_bp.route("/<int:categoria_id>/excluir", methods=["POST"])
def excluir(categoria_id):
    """
    Remove uma categoria existente.
    """

    try:
        excluir_categoria(categoria_id)
    except CategoriaNaoEncontradaError:
        # Se a categoria já não existe (ex: excluída em outra aba),
        # simplesmente seguimos para a listagem sem quebrar a página.
        pass

    return redirect(url_for("categoria.listar"))
