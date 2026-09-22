"""
Testes de persistência.
"""

from datetime import date
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

import pytest

from app import create_app
from app.extensions import db
from app.models.transacao import Transacao
from app.domain.credito import Credito
from app.mappers.transacao_mapper import (
    to_model,
    CategoriaDaTransacaoNaoEncontradaError,
)
from app.domain.categoria import Categoria as CategoriaDomain
from app.domain.emprestimo import Emprestimo as EmprestimoDomain
from app.mappers.categoria_mapper import to_model as categoria_to_model
from app.mappers.emprestimo_mapper import to_model as emprestimo_to_model
from app.models.categoria import Categoria
from app.models.emprestimo import Emprestimo as EmprestimoModel


@pytest.fixture
def app():
    """
    Cria uma aplicação Flask configurada para testes.
    """

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

def test_deve_persistir_transacao(app):
    """
    Verifica se uma transação pode ser gravada no banco.
    """

    categoria = Categoria(nome="Salário", tipo="credito")
    db.session.add(categoria)
    db.session.commit()

    transacao = Transacao(
        tipo="credito",
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria_id=categoria.id,
        comprovante=None,
    )

    db.session.add(transacao)
    db.session.commit()

    assert transacao.id is not None

def test_deve_recuperar_transacao_persistida(app):
    """
    Verifica se uma transação pode ser recuperada do banco.
    """

    categoria = Categoria(nome="Salário", tipo="credito")
    db.session.add(categoria)
    db.session.commit()

    transacao = Transacao(
        tipo="credito",
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria_id=categoria.id,
        comprovante=None,
    )

    db.session.add(transacao)
    db.session.commit()

    transacao_salva = db.session.get(
        Transacao,
        transacao.id,
    )

    assert transacao_salva is not None
    assert transacao_salva.tipo == "credito"
    assert transacao_salva.descricao == "Salário"
    assert transacao_salva.valor == Decimal("5000.00")
    assert transacao_salva.data == date(2026, 9, 5)
    assert transacao_salva.categoria.nome == "Salário"
    assert transacao_salva.comprovante is None

def test_deve_persistir_credito_do_dominio(app):
    """
    Verifica se um Crédito de domínio pode ser convertido e
    persistido no banco.
    """

    categoria = Categoria(nome="Salário", tipo="credito")
    db.session.add(categoria)
    db.session.commit()

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Salário",
    )

    modelo = to_model(credito)

    db.session.add(modelo)
    db.session.commit()

    assert modelo.id is not None

    transacao_salva = db.session.get(
        Transacao,
        modelo.id,
    )

    assert transacao_salva is not None
    assert transacao_salva.tipo == "credito"
    assert transacao_salva.descricao == "Salário"
    assert transacao_salva.valor == Decimal("5000.00")
    assert transacao_salva.categoria.nome == "Salário"

def test_nao_deve_converter_transacao_com_categoria_inexistente(app):
    """
    Verifica se o mapper rejeita converter uma transação cuja
    categoria não está cadastrada.
    """

    credito = Credito(
        descricao="Salário",
        valor=Decimal("5000.00"),
        data=date(2026, 9, 5),
        categoria="Categoria Inexistente",
    )

    with pytest.raises(CategoriaDaTransacaoNaoEncontradaError):
        to_model(credito)

def test_nao_deve_persistir_tipo_invalido(app):
    """
    Verifica se o banco rejeita um tipo de transação inválida.
    """

    categoria = Categoria(nome="Teste", tipo="credito")
    db.session.add(categoria)
    db.session.commit()

    transacao = Transacao(
        tipo="banana",
        descricao="Teste",
        valor=Decimal("1000.00"),
        data=date(2026, 9, 13),
        categoria_id=categoria.id,
    )

    db.session.add(transacao)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()

def test_deve_persistir_categoria(app):
    """
    Verifica se uma categoria pode ser gravada no banco.
    """

    categoria = Categoria(nome="Salário", tipo="credito")

    db.session.add(categoria)
    db.session.commit()

    assert categoria.id is not None

def test_deve_persistir_categoria_do_dominio(app):
    """
    Verifica se uma Categoria de domínio pode ser convertida
    e persistida no banco.
    """

    categoria = CategoriaDomain(nome="Aluguel", tipo="debito")

    modelo = categoria_to_model(categoria)

    db.session.add(modelo)
    db.session.commit()

    assert modelo.id is not None

def test_nao_deve_permitir_categoria_duplicada_no_mesmo_tipo(app):
    """
    Verifica se o banco rejeita duas categorias com o mesmo
    nome e o mesmo tipo.
    """

    db.session.add(Categoria(nome="Salário", tipo="credito"))
    db.session.commit()

    db.session.add(Categoria(nome="Salário", tipo="credito"))

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()

def test_deve_permitir_mesmo_nome_em_tipos_diferentes(app):
    """
    Verifica se o mesmo nome de categoria pode existir em
    tipos diferentes (credito e debito).
    """

    db.session.add(Categoria(nome="Outros", tipo="credito"))
    db.session.add(Categoria(nome="Outros", tipo="debito"))
    db.session.commit()

    categorias = db.session.query(Categoria).all()

    assert len(categorias) == 2

def test_deve_persistir_emprestimo_com_suas_parcelas(app):
    """
    Verifica se um empréstimo e suas parcelas são persistidos juntos no banco.
    """

    emprestimo = EmprestimoDomain(
        descricao="Empréstimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1),
    )

    modelo = emprestimo_to_model(emprestimo)

    db.session.add(modelo)
    db.session.commit()

    assert modelo.id is not None

    emprestimo_salvo = db.session.get(EmprestimoModel, modelo.id)

    assert emprestimo_salvo is not None
    assert len(emprestimo_salvo.parcelas) == 3

def test_excluir_emprestimo_deve_excluir_suas_parcelas_em_cascata(app):
    """
    Verifica se excluir um empréstimo remove tamvém todas as suas parcelas (cascade delete-orphan).
    """

    from app.models.parcela import Parcela as ParcelaModel

    emprestimo = EmprestimoDomain(
        descricao="Empréstimo pessoal",
        valor_retirado=Decimal("5000.00"),
        taxa_juros_mensal=Decimal("0.02"),
        quantidade_parcelas=3,
        data_contratacao=date(2026, 9, 1)
    )

    modelo = emprestimo_to_model(emprestimo)

    db.session.add(modelo)
    db.session.commit()

    emprestimo_id = modelo.id

    db.session.delete(modelo)
    db.session.commit()

    parcelas_restantes = (
        db.session.query(ParcelaModel)
        .filter_by(emprestimo_id=emprestimo_id)
        .count()
    )

    assert parcelas_restantes == 0
