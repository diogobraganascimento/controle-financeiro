"""
Serviços de aplicação para Empréstimo.

Este módulo orquestra a criação, consulta e o pagamento de parcelas de parcelas de empréstimos, conectando o domínio, o mapper e a persistência.
"""

from datetime import date
from decimal import Decimal

from app.domain.emprestimo import Emprestimo as EmprestimoDomain
from app.extensions import db
from app.mappers.emprestimo_mapper import to_domain, to_model
from app.models.emprestimo import Emprestimo as EmprestimoModel
from app.models.parcela import Parcela as ParcelaModel


class EmprestimoNaoEncontradoError(Exception):
    """
    Levantada quando nenhum empréstimo é encontrado com o id informado.
    """

class ParcelaNaoEncontradaError(Exception):
    """
    Levantado quando nenhuma parcela com o número informado é encontrada no empréstimo.
    """

def listar_emprestimos() -> list[EmprestimoDomain]:
    """
    Retorna todos os empréstimos cadastrados, da contratação mais recente para a mais antiga.
    """

    modelos = (
        db.session.query(EmprestimoModel)
        .order_by(EmprestimoModel.data_contratacao.desc())
        .all()
    )

    return [to_domain(modelo) for modelo in modelos]

def obter_emprestimo(emprestimo_id: int) -> EmprestimoDomain:
    """
    Busca um empréstimo pelo id, com suas parcelas.
    
    Levanta EmprestimoNaoEncontradoErro se não existir nenhum empréstimo com esse id.
    """

    modelo = db.session.get(EmprestimoModel, emprestimo_id)

    if modelo is None:
        raise EmprestimoNaoEncontradoError(
            f"Empréstimo com id {emprestimo_id} não encontrado."
        )

    return to_domain(modelo)

def criar_emprestimo(
        descricao: str,
        valor_retirado: Decimal,
        taxa_juros_mensal: Decimal,
        quantidade_parcelas: int,
        data_contratacao: date,
) -> EmprestimoDomain:
    """
    Cria e persiste um novo empréstimo, com suas parcelas geradas automaticamente pelo Sistema Price.
    """

    emprestimo = EmprestimoDomain(
        descricao=descricao,
        valor_retirado=valor_retirado,
        taxa_juros_mensal=taxa_juros_mensal,
        quantidade_parcelas=quantidade_parcelas,
        data_contratacao=data_contratacao,
    )

    modelo = to_model(emprestimo)

    db.session.add(modelo)
    db.session.commit()

    return to_domain(modelo)

def pagar_parcela(emprestimo_id: int, numero_parcela: int) -> None:
    """
    Marca uma parcela específica de um empréstimo como paga.
    
    Levanta EmprestimoNaoEncontradoError se o empréstimo não existir, e ParcelaNaoEncontradaError se o número da parcela não existir nesse empréstimo.
    """

    modelo = db.session.get(EmprestimoModel, emprestimo_id)

    if modelo is None:
        raise EmprestimoNaoEncontradoError(
            f"Empréstimo com id {emprestimo_id} não encontrado."
        )

    parcela_model = next(
        (p for p in modelo.parcelas if p.numero == numero_parcela),
        None
    )

    if parcela_model is None:
        raise ParcelaNaoEncontradaError(
            f"Parcela número {numero_parcela} não encontrada "
            f"no empréstimo {emprestimo_id}."
        )

    parcela_model.paga = True

    db.session.commit()
