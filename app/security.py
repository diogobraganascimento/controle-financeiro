"""
Integração com Flask-Login.

Este módulo adapta a entidade de domínio Usuario para a interface
que o Flask-Login espera (UserMixin), e registra a função que
recarrega o usuário logado a cada requisição, a partir do id
guardado na sessão.
"""

from flask_login import UserMixin

from app.extensions import login_manager
from app.services.auth_service import (
    UsuarioNaoEncontradoError,
    obter_usuario_por_id,
)

class UsuarioSession(UserMixin):
    """
    Representa o usuário autenticado na sessão do Flask-Login.

    Envolve a entidade de domínio Usuario, expondo apenas o
    necessário para o Flask-Login (o atributo `id`, usado por
    UserMixin.get_id()).
    """

    def __init__(self, usuario):
        self.id = usuario.id
        self.username = usuario.username

@login_manager.user_loader
def carregar_usuario(usuario_id: str):
    """
    Recarrega o usuário logado a cada requisição, a partir do
    id guardado na sessão. Retorna None se o id não corresponder
    a nenhum usuário existente (a sessão é então invalidada
    automaticamente pelo Flask-Login).
    """

    try:
        usuario = obter_usuario_por_id(int(usuario_id))
    except UsuarioNaoEncontradoError:
        return None

    return UsuarioSession(usuario)
