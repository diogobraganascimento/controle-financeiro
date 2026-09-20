"""
Fábrica de blueprints para Crédito e Débito.

Crédito e Débito têm rotas quase idênticas: mesmos campos, mesmo
fluxo de cadastro, listagem, edição e exclusão, diferindo apenas
na classe de domínio usada e no tipo da transação. Em vez de
duplicar esse código duas vezes, esta função constrói um Blueprint
parametrizado, reaproveitado por app/routes/credito.py e
app/routes/debito.py.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, redirect, render_template, request, url_for

from app.mappers.transacao_mapper import CategoriaDaTransacaoNaoEncontradaError
from app.services.categoria_service import listar_categorias_por_tipo
from app.services.transacao_service import (
    TransacaoNaoEncontradaError,
    atualizar_transacao,
    criar_transacao,
    excluir_transacao,
    listar_transacoes,
    obter_transacao,
)


def _analisar_formulario(form) -> dict:
    """
    Extrai e converte os campos do formulário de transação.

    Retorna um dicionário com os dados já convertidos. Se algum
    campo não puder ser convertido, o dicionário traz a chave
    "erro" com uma mensagem amigável, e "valor"/"data" ficam
    ausentes.
    """

    dados = {
        "descricao": form.get("descricao", ""),
        "categoria": form.get("categoria", ""),
        "valor_texto": form.get("valor", ""),
        "data_texto": form.get("data", ""),
        "comprovante": form.get("comprovante") or None,
    }

    try:
        dados["valor"] = Decimal(dados["valor_texto"])
    except InvalidOperation:
        dados["erro"] = "Valor inválido."
        return dados

    try:
        dados["data"] = date.fromisoformat(dados["data_texto"])
    except ValueError:
        dados["erro"] = "Data inválida."
        return dados

    return dados


def criar_blueprint_transacao(
    nome: str,
    classe,
    tipo: str,
    url_prefix: str,
    template_dir: str,
) -> Blueprint:
    """
    Constrói um Blueprint completo de CRUD para uma classe de
    transação.

    Args:
        nome: nome do blueprint (ex: "credito"), usado em url_for.
        classe: Credito ou Debito — a classe de domínio instanciada.
        tipo: "credito" ou "debito" — usado para filtrar consultas.
        url_prefix: prefixo das rotas (ex: "/creditos").
        template_dir: pasta de templates (ex: "creditos").
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
            dados = _analisar_formulario(request.form)

            if "erro" in dados:
                return render_template(
                    f"{template_dir}/nova.html",
                    erro=dados["erro"],
                    categorias=categorias,
                    descricao=dados["descricao"],
                    valor=dados["valor_texto"],
                    data=dados["data_texto"],
                    categoria=dados["categoria"],
                )

            try:
                criar_transacao(
                    classe=classe,
                    descricao=dados["descricao"],
                    valor=dados["valor"],
                    data=dados["data"],
                    categoria=dados["categoria"],
                    comprovante=dados["comprovante"],
                )
            except (
                ValueError,
                TypeError,
                CategoriaDaTransacaoNaoEncontradaError,
            ) as erro:
                return render_template(
                    f"{template_dir}/nova.html",
                    erro=str(erro),
                    categorias=categorias,
                    descricao=dados["descricao"],
                    valor=dados["valor_texto"],
                    data=dados["data_texto"],
                    categoria=dados["categoria"],
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

    @bp.route("/<int:transacao_id>/editar", methods=["GET", "POST"])
    def editar(transacao_id):
        categorias = listar_categorias_por_tipo(tipo)

        try:
            transacao_atual = obter_transacao(transacao_id)
        except TransacaoNaoEncontradaError as erro:
            return render_template(
                f"{template_dir}/listar.html",
                transacoes=listar_transacoes(tipo),
                erro=str(erro),
            )

        if request.method == "POST":
            dados = _analisar_formulario(request.form)

            if "erro" in dados:
                return render_template(
                    f"{template_dir}/editar.html",
                    erro=dados["erro"],
                    categorias=categorias,
                    transacao_id=transacao_id,
                    descricao=dados["descricao"],
                    valor=dados["valor_texto"],
                    data=dados["data_texto"],
                    categoria=dados["categoria"],
                )

            try:
                atualizar_transacao(
                    transacao_id=transacao_id,
                    classe=classe,
                    descricao=dados["descricao"],
                    valor=dados["valor"],
                    data=dados["data"],
                    categoria=dados["categoria"],
                    comprovante=dados["comprovante"],
                )
            except (
                ValueError,
                TypeError,
                CategoriaDaTransacaoNaoEncontradaError,
            ) as erro:
                return render_template(
                    f"{template_dir}/editar.html",
                    erro=str(erro),
                    categorias=categorias,
                    transacao_id=transacao_id,
                    descricao=dados["descricao"],
                    valor=dados["valor_texto"],
                    data=dados["data_texto"],
                    categoria=dados["categoria"],
                )

            return redirect(url_for(f"{nome}.listar"))

        return render_template(
            f"{template_dir}/editar.html",
            erro=None,
            categorias=categorias,
            transacao_id=transacao_id,
            descricao=transacao_atual.descricao,
            valor=str(transacao_atual.valor),
            data=transacao_atual.data.isoformat(),
            categoria=transacao_atual.categoria,
        )

    @bp.route("/<int:transacao_id>/excluir", methods=["POST"])
    def excluir(transacao_id):
        try:
            excluir_transacao(transacao_id)
        except TransacaoNaoEncontradaError:
            # Se a transação já não existe (ex: excluída em outra
            # aba), simplesmente seguimos para a listagem.
            pass

        return redirect(url_for(f"{nome}.listar"))

    return bp