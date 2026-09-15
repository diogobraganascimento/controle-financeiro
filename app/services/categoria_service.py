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

