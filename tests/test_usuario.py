"""
Testes da entidade de domínio Usuario.
"""

import pytest

from app.domain.usuario import Usuario


def test_deve_criar_usuario_com_senha_hasheada():
    """
    Verifica se a senha nunca é armazenada em texto puro.
    """

    usuario = Usuario.criar(username="dnascimento", senha="senha1234")

    assert usuario.username == "dnascimento"
    assert usuario.senha_hash != "senha1234"

def test_deve_verificar_senha_correta():
    """
    Verifica se a senha correta é validada com sucesso.
    """

    usuario = Usuario.criar(username="dnascimento", senha="senha1234")

    assert usuario.verificar_senha("senha1234") is True

def test_deve_rejeitar_senha_incorreta():
    """
    Verifica se uma senha incorreta é rejeitada.
    """

    usuario = Usuario.criar(username="dnascimento", senha="senha1234")

    assert usuario.verificar_senha("outrasenha") is False

def test_deve_rejeitar_senha_curta():
    """
    Verifica se uma senha com menos de 8 caracteres é rejeitada.
    """

    with pytest.raises(ValueError):
        Usuario.criar(username="dnascimento", senha="123")

def test_deve_rejeitar_username_vazio():
    """
    Verifica se um username vazio é rejeitado.
    """

    with pytest.raises(ValueError):
        Usuario(username="", senha_hash="hash-qualquer")
