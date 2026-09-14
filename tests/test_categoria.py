"""
Testes da entidade de domínio Categoria.
"""

import pytest

from app.domain.categoria import Categoria


def test_deve_criar_categoria_valida():
    """
    Verifica se uma categoria válida é criada corretamente.
    """

    categoria = Categoria(nome="Salário", tipo="credito")

    assert categoria.nome == "Salário"
    assert categoria.tipo == "credito"

def test_deve_remover_espacos_do_nome():
    """
    Verifica se espaços extras nas bordas do nome são removidos.
    """

    categoria = Categoria(nome="  Aluguel  ", tipo="debito")

    assert categoria.nome == "Aluguel"

def test_deve_rejeitar_nome_vazio():
    """
    Verifica se um nome vazio é rejeitado.
    """

    with pytest.raises(ValueError):
        Categoria(nome="", tipo="credito")

def test_deve_rejeitar_nome_com_apenas_espacos():
    """
    Verifica se um nome contendo apenas espaços é rejeitado.
    """

    with pytest.raises(ValueError):
        Categoria(nome="    ", tipo="credito")

def test_deve_rejeitar_nome_que_nao_seja_string():
    """
    Verifica se um nome que não seja string é rejeitado.
    """

    with pytest.raises(TypeError):
        Categoria(nome=123, tipo="credito")

def test_deve_rejeitar_tipo_invalido():
    """
    Verifica se um tipo fora de "credito"/"debito" é rejeitado.
    """

    with pytest.raises(ValueError):
        Categoria(nome="Salário", tipo="tranferencia")

def test_deve_rejeitar_tipo_que_nao_seja_string():
    """
    Verifica se um tipo que não seja string é rejeitado.
    """

    with pytest.raises(TypeError):
        Categoria(nome="Salário", tipo=123)

def test_deve_permitir_alterar_nome():
    """
    Verifica se o nome pode ser alterado para um valor válido.
    """

    categoria = Categoria(nome="Salário", tipo="credito")
    categoria.nome = "Renda Extra"

    assert categoria.nome == "Renda Extra"

def test_nao_deve_permitir_alterar_nome_para_vazio():
    """
    Varifica se o nome não pode ser alterado para um valor vazio.
    """

    categoria = Categoria(nome="Salário", tipo="credito")

    with pytest.raises(ValueError):
        categoria.nome = ""
