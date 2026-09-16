"""
Testes dos mapeamentos entre domínio e persistência para categorias.
"""

from app.domain.categoria import Categoria as CategoriaDomain
from app.mappers.categoria_mapper import to_domain, to_model
from app.models.categoria import Categoria as CategoriaModel


def test_deve_converter_categoria_para_modelo_de_persistencia():
    """
    VErifica se uma Categoria de domínio é convertida corretamente para o modelo SQLalchemy.
    """

    categoria = CategoriaDomain(nome="Salário", tipo="credito")

    modelo = to_model(categoria)

    assert modelo.nome == "Salário"
    assert modelo.tipo == "credito"

def test_deve_converter_modelo_de_categoria_para_dominio():
    """
    Verifica se um modelo de persistência de categoria é convertido para a entidade de domínio correta.
    """

    modelo = CategoriaModel(nome="Aluguel", tipo="debito")

    categoria = to_domain(modelo)

    assert isinstance(categoria, CategoriaDomain)
    assert categoria.nome == "Aluguel"
    assert categoria.tipo == "debito"

def test_to_domain_deve_preservar_o_id():
    """
    Verifica se o id do modelo é propagado para a entidade de domínio ao converter.
    """

    modelo = CategoriaModel(nome="Salário", tipo="credito")
    modelo.id = 42

    categoria = to_domain(modelo)

    assert categoria.id == 42
