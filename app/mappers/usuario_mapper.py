"""
Mapeamento entre entidade de domínio e modelo de persistência para o usuário do sistema.
"""

from app.domain.usuario import Usuario as UsuarioDomain
from app.models.usuario import Usuario as UsuarioModel


def to_model(usuario: UsuarioDomain) -> UsuarioModel:
    """
    Converte um usuário de domínio em modelo de persistência.
    """

    return UsuarioModel(
        username=usuario.username,
        senha_hash=usuario.senha_hash,
    )

def to_domain(usuario: UsuarioModel) -> UsuarioDomain:
    """
    Converte um modelo de persistência em uma entidade de domínio.
    """

    return UsuarioDomain(
        username=usuario.username,
        senha_hash=usuario.senha_hash,
        id=usuario.id,
    )
