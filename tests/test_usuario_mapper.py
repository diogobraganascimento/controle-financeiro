"""
Testes dos mapeamentos entre domínio e persistência para o
usuário do sistema.
"""

from app.domain.usuario import Usuario as UsuarioDomain
from app.mappers.usuario_mapper import to_domain, to_model
from app.models.usuario import Usuario as UsuarioModel

def test_deve_converter_usuario_para_modelo_de_persistencia():
    """
    Verifica se um usuário de domínio é convertido corretamente para o modelo SQLalchemy.
    """

    usuario = UsuarioDomain.criar(username="dnascimento", senha="senha1234")

    modelo = to_model(usuario)

    assert modelo.username == "dnascimento"
    assert modelo.senha_hash == usuario.senha_hash

def test_deve_converte_modelo_de_usuario_para_dominio():
    """
    Verifica se um modelo de persistência de usuário é convertido para a entidade de 
    domínio correta.
    """

    modelo = UsuarioModel(username="dnascimento", senha_hash="hash-qualquer")

    usuario = to_domain(modelo)

    assert isinstance(usuario, UsuarioDomain)
    assert usuario.username == "dnascimento"
