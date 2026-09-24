"""
Rotas para gerenciamento de Empréstimo.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, redirect, render_template, request, url_for

from app.services.emprestimo_service import (
    EmprestimoNaoEncontradoError,
    ParcelaNaoEncontradaError,
    criar_emprestimo,
    listar_emprestimos,
    obter_emprestimo,
    pagar_parcela,
)

emprestimo_bp = Blueprint(
    "emprestimo",
    __name__,
    url_prefix="/emprestimos",
)

@emprestimo_bp.route("/", methods=["GET"])
def listar():
    """
    Exibe a lista de empréstimos cadastrados.
    """

    emprestimos = listar_emprestimos()

    return render_template(
        "emprestimos/listar.html",
        emprestimos=emprestimos,
    )

@emprestimo_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """
    Exibe o formulário de cadastro (GET) e processa o cadastro de um novo empréstimo (POST).
    """

    if request.method == "POST":
        descricao = request.form.get("descricao", "")
        valor_retirado_texto = request.form.get("valor_retirado", "")
        # A taxa é digitada em procentagem (ex: "2" para 2%) e
        # convertida para decimal (0.02) antes de chegar ao domínio.
        taxa_percentual_texto = request.form.get("taxa_juros_mensal", "")
        quantidade_texto = request.form.get("quantidade_parcelas", "")
        data_texto = request.form.get("data_contratacao", "")

        campos_formulario = {
            "descricao": descricao,
            "valor_retirado": valor_retirado_texto,
            "taxa_juros_mensal": taxa_percentual_texto,
            "quantidade_parcelas": quantidade_texto,
            "data_contratacao": data_texto,
        }

        try:
            valor_retirado = Decimal(valor_retirado_texto)
            taxa_percentual = Decimal(taxa_percentual_texto)
            taxa_juros_mensal = taxa_percentual / Decimal("100")
        except InvalidOperation:
            return render_template(
                "emprestimos/novo.html",
                erro="Valor retirado ou taxa de juros inválidos.",
                **campos_formulario,
            )

        try:
            quantidade_parcelas = int(quantidade_texto)
        except ValueError:
            return render_template(
                "emprestimos/novo.html",
                erro="Quantidade de parcelas inválida.",
                **campos_formulario,
            )

        try:
            data_contratacao = date.fromisoformat(data_texto)
        except ValueError:
            return render_template(
                "emprestimos/novo.html",
                erro="Data de contratação inválida.",
                **campos_formulario,
            )

        try:
            criar_emprestimo(
                descricao=descricao,
                valor_retirado=valor_retirado,
                taxa_juros_mensal=taxa_juros_mensal,
                quantidade_parcelas=quantidade_parcelas,
                data_contratacao=data_contratacao,
            )
        except (ValueError, TypeError) as erro:
            return render_template(
                "emprestimos/novo.html",
                erro=str(erro),
                **campos_formulario,
            )

        return redirect(url_for("emprestimo.listar"))

    return render_template(
        "emprestimos/novo.html",
        erro=None,
        descricao="",
        valor_retirado="",
        taxa_juros_mensal="",
        quantidade_parcelas="",
        data_contratacao="",
    )

@emprestimo_bp.route("/<int:emprestimo_id>", methods=["GET"])
def detalhe(emprestimo_id):
    """
    Exibe os detalhes de um empréstimo, incluindo todas as suas parcelas.
    """

    try:
        emprestimo = obter_emprestimo(emprestimo_id)
    except EmprestimoNaoEncontradoError as erro:
        return render_template(
            "emprestimos/novo.html",
            emprestimo=listar_emprestimos(),
            erro=str(erro),
        )

    return render_template(
        "emprestimos/detalhe.html",
        emprestimo=emprestimo,
    )

@emprestimo_bp.route("/<int:emprestimo_id>/parcelas/<int:numero_parcela>/pagar", methods=["POST"])
def pagar(emprestimo_id, numero_parcela):
    """
    Marca uma parcela específica do empréstimo como paga.
    """

    try:
        pagar_parcela(emprestimo_id, numero_parcela)
    except (EmprestimoNaoEncontradoError, ParcelaNaoEncontradaError):
        # Se o empréstimo ou a parcela não existem mais (ex: alterado em outra aba),
        # simplesmente seguimos para o detalhe sem quebrar a página.
        pass

    return redirect(url_for("emprestimo.detalhe", emprestimo_id=emprestimo_id))
