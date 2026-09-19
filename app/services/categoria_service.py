"""
Serviços de aplicação para Categoria.

Este módulo orquestra a criação e consulta de categorias, conectando o domínio, o mapper e a persistência. As rotas Flask não devem falar diretamente com o banco de dados nem com os mappers - elas chamam este serviço.
"""

from sqlalchemy.exc import IntegrityError

from app.domain.categoria import Categoria as CategoriaDomain
from app.extensions import db
from app.mappers.categoria_mapper import to_domain, to_model
from app.models.categoria import Categoria as CategoriaModel


class CategoriaJaExisteError(Exception):
    """
    Levantada quando já existe uma categoria com o mesmo nome e o mesmo tipo.
    """

class CategoriaNaoEncontradaError(Exception):
    """
    Levantada quand nenhuma categoria é encontrada com o id informado.
    """

def listar_categorias() -> list[CategoriaDomain]:
    """
    Retorna todas as categorias cadastradas, já convertidas para entidades de domínio.
    """

    modelos = (
        db.session.query(CategoriaModel)
        .order_by(CategoriaModel.tipo, CategoriaModel.nome)
        .all()
    )

    return [to_domain(modelo) for modelo in modelos]

def listar_categorias_por_tipo(tipo: str) -> list[CategoriaDomain]:
    """
    Retorna as categorias cadastradas de um tipo específico (credito ou debito).
    
    Usada pelos formulários de Crédito/Débito, que só devem ogerecer categorias compatíveis com o tipo da transação.
    """

    modelos = (
        db.session.query(CategoriaModel)
        .filter_by(tipo=tipo)
        .order_by(CategoriaModel.nome)
        .all()
    )

    return [to_domain(modelo) for modelo in modelos]

def obter_categoria(categoria_id: int) -> CategoriaDomain:
    """
    Busca uma categoria pelo id.
    
    Levanta CategoriaNaoEcontradaError se não existir nenhuma categoria com ese id.
    """

    modelo = db.session.get(CategoriaModel, categoria_id)

    if modelo is None:
        raise CategoriaNaoEncontradaError(
            f"Categoria com id {categoria_id} não encontrada."
        )

    return to_domain(modelo)

def criar_categoria(nome: str, tipo: str) -> CategoriaDomain:
    """
    Cria e persiste uma nova categoria.
        
    Levanta ValueError ou TypeError se os dados forem inválidos (regra de domínio), eCategoriaJaExisteError se já existir uma categoria com o mesmo nome e tipo.
    """

    # A validação de nogócio (nome obrigatório, tipo válido)
    # acontece aqui, dentro do construtor da entidade de domínio.
    categoria = CategoriaDomain(nome=nome, tipo=tipo)

    modelo = to_model(categoria)

    db.session.add(modelo)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        raise CategoriaJaExisteError(
            f"Já existe uma categoria '{categoria.nome}' "
            f"do tipo '{categoria.tipo}'."
        )

    return to_domain(modelo)

def atualizar_categoria(
        categoria_id: int,
        nome: str,
        tipo: str,
) -> CategoriaDomain:
    """
    Atualiza o nome e o tipo de uma categoria existente.
    
    Levanta CategoriaNaoEncontradaError se o id não existir, ValueError/TypeError se os novos dados forem inválidos, e CategoriaJaExistieError se a alteração colidir com outras categorias já cadastradas.
    """

    modelo = db.session.get(CategoriaModel, categoria_id)

    if modelo is None:
        raise CategoriaNaoEncontradaError(
            f"Categoria com id {categoria_id} não encontrada."
        )

    # Reaproveita as validações de domínio antes de alterar o modelo.
    categoria_validada = CategoriaDomain(nome=nome, tipo=tipo)

    modelo.nome = categoria_validada.nome
    modelo.tipo = categoria_validada.tipo

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        raise CategoriaJaExisteError(
            f"Já existe uma categoria '{categoria_validada.nome}' "
            f"do tipo '{categoria_validada.tipo}'."
        )

    return to_domain(modelo)

def excluir_categoria(categoria_id: int):
    """
    Remove uma categoria pelo id.
    
    Levanta CategoriaNaoEncontradaError se o id não existir.
    """

    modelo = db.session.get(CategoriaModel, categoria_id)

    if modelo is None:
        raise CategoriaNaoEncontradaError(
            f"Categoria com id {categoria_id} não encontrada."
        )

    db.session.delete(modelo)
    db.session.commit()
