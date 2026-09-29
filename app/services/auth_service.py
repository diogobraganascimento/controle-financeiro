"""
Serviço de autenticação do usuário único do sistema.
"""

from sqlalchemy.exc import IntegrityError

from app.domain.usuario import Usuario as UsuarioDomain
from app.extensions import db
from app.mappers.usuario_mapper import to_domain, to_model
from app.models.usuario import Usuario as UsuarioModel


class CredenciaisInvalidasError(Exception):
    """
    Levantada quando o username ou a senha estão incorretos.
    """

class UsuarioNaoEncontradoError(Exception):
    """
    Levantada quando nenhum usuário é encontrado com o id informado.
    """

class UsuarioJaExisteError(Exception):
    """
    Levantada ao tentar criar um usuário com um username já cadastrado.
    """

def criar_usuario(username: str, senha: str) -> UsuarioDomain:
    """
    Cria e persiste o usuário do sistema.
    
    Usado apenas pelo comando de terminal (flask criar-usuario), já que este projeto não tem cadastro público
    de usuários (sistema de usuário único, decisão registrada no módulo de autenticação).
    """

    usuario = UsuarioDomain.criar(username=username, senha=senha)

    modelo = to_model(usuario)

    db.session.add(modelo)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        raise UsuarioJaExisteError(
            f"Já existe um usuário com o username '{username}'."
        )

    return to_domain(modelo)

def autenticar(username: str, senha: str) -> UsuarioDomain:
    """
    Verifica as credenciais informadas e retorna o usuário
    correspondente.

    Levanta CredenciaisInvalidasError tanto se o username não
    existir quanto se a senha estiver incorreta — de propósito,
    a mensagem não diferencia os dois casos, para não revelar a
    quem tenta invadir se um username específico existe ou não.
    """

    modelo = (
        db.session.query(UsuarioModel)
        .filter_by(username=username)
        .first()
    )

    if modelo is None:
        raise CredenciaisInvalidasError("Usuário ou senha inválidos.")

    usuario = to_domain(modelo)

    if not usuario.verificar_senha(senha):
        raise CredenciaisInvalidasError("Usuário ou senha inválidos.")

    return usuario

def obter_usuario_por_id(usuario_id: int) -> UsuarioDomain:
    """
    Busca um usuário pelo id.
    
    Usado pelo user_loader do Flask-Login, que recarregar o usuário logado a partir do id guardado
    na sessão, a cada requisição.
    """

    modelo = db.session.get(UsuarioModel, usuario_id)

    if modelo is None:
        raise UsuarioNaoEncontradoError(
            f"Usuário com id{usuario_id} não encontrado."
        )

    return to_domain(modelo)
