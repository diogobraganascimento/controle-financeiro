"""
Fábrica de blueprints para Crédito e Débito.

Crédito e Débito têm rotas quase idênticas: Mesmos campos, mesmo fluxo de cadastro e listagem, diferindo apenas na classe de domínio usada e no tipo da transação. Em vez de dubplicar esse código duas vezes, esta função constrói um Blueprint parametrizado, reaproveitando por app/routes/credito.py e app/routes/debito.py.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, redirect, render_template, request, url_for

from app.mappers.transacao_mapper import CategoriaDaTransacaoNaoEncontradaError
from app.services.categoria_service import listar_categorias_por_tipo
from app.services.transacao_service import criar_transacao, listar_transacoes


def criar_blueprint_transacao(
        nome: str,
        classe,
        tipo: str,
        url_prefix: str,
        template_dir: str,
) -> Blueprint:
    """
    Constrói um Blueprint completo de CRUD (Create + Read) para uma classe de transação.
    
    args:
        nome: nome do blueprint (ex: "credito"), usado em url_for.
        classe: Credito ou Debito - a classe de domínio instanciada.
        tipo: "credito" ou "debito" - usado para filtrar consultas.
        url_prefix: prefixo das rotas (ex: "/creditos").
        template_dir: pasta de template (ex: "creditos").
    """

    bp = Blueprint(nome, __name__, url_prefix=url_prefix)

    @bp.route("/", methods=["GET"])
    def listar():
        transacoes = listar_transacoes(tipo)

        return render_template(
            f"{template_dir}/listar.html",
            transacoes=transacoes,
        )

    @bp.route("/novo", methods=["GET", "POST"])
    def nova():
        categorias = listar_categorias_por_tipo(tipo)

        if request.method == "POST":
            descricao = request.form.get("descricao", "")
            categoria_nome = request.form.get("categoria", "")
            valor_texto = request.form.get("valor", "")
            data_texto = request.form.get("data", "")
            comprovante = request.form.get("comprovante") or None

            try:
                valor = Decimal(valor_texto)
            except InvalidOperation:
                return render_template(
                    f"{template_dir}/nova.html",
                    erro="valor inválido.",
                    categorias=categorias,
                    descricao=descricao,
                    valor=valor_texto,
                    data=data_texto,
                    categoria=categoria_nome,
                )

            try:
                data_transacao = date.fromisoformat(data_texto)
            except ValueError:
                return render_template(
                    f"{template_dir}/nova.html",
                    erro="Data inválida.",
                    categorias=categorias,
                    descricao=descricao,
                    valor=valor_texto,
                    data=data_texto,
                    categoria=categoria_nome,
                )

            try:
                criar_transacao(
                    classe=classe,
                    descricao=descricao,
                    valor=valor,
                    data=data_transacao,
                    categoria=categoria_nome,
                    comprovante=comprovante,
                )
            except(ValueError, TypeError, CategoriaDaTransacaoNaoEncontradaError,) as erro:
                return render_template(
                    f"{template_dir}/nova.html",
                    erro=str(erro),
                    categorias=categorias,
                    descricao=descricao,
                    valor=valor_texto,
                    categoria=categoria_nome,
                )

            return redirect(url_for(f"{nome}.listar"))

        return render_template(
            f"{template_dir}/nova.html",
            erro=None,
            categorias=categorias,
            descricao="",
            valor="",
            data="",
            categoria="",
        )

    return bp
