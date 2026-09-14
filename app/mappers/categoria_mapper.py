"""
Mapeamento entre entidades de domínio e modelos de persistência para categorias financeiras.
"""

from app.domain.categoria import Categoria as CategoriaDomain
from app.models.categoria import Categoria as CategoriaModel


def to_model(categoria: CategoriaDomain) -> CategoriaModel:
    """
    Converte uma categoria de domínio em um modelo de persistência.
    """

    return CategoriaModel(
        nome=categoria.nome,
        tipo=categoria.tipo,
    )

def to_domain(categoria: CategoriaModel) -> CategoriaDomain:
    """
    Converte um modelo de persistência em uma entidade de Domínio.
    """

    return CategoriaDomain(
        nome=categoria.nome,
        tipo=categoria.tipo
    )
