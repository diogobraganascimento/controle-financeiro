"""
Inicialização da aplicação Flask.
"""

import click
from flask import Flask, request
from flask_login import login_required

from app.config import Config
from app.extensions import db, login_manager
from app.routes.auth import auth_bp
from app.routes.home import home_bp
from app.routes.categoria import categoria_bp
from app.routes.credito import credito_bp
from app.routes.debito import debito_bp
from app.routes.emprestimo import emprestimo_bp


@login_required
def _verificar_login():
    """
    Função "vazia" usada como gancho para o decorator
    login_required em before_request: se o usuário não estiver
    autenticado, login_required intercepta a requisição e
    redireciona para o login antes mesmo desta função rodar.
    """

    return None

def create_app(test_config=None):
    """
    Cria e configura uma instancia da aplicação Flask.

    Args:
        test_config: Configurações opcionais para testes.

    returns:
        Flask: aplicação Flask configurada.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config is not None:
        app.config.from_mapping(test_config)

    # Em modo de teste, a autenticação fica desabilitada por padrão,
    # para que os testes de regras de negócio não precisem fazer login
    # em cada um. Um teste pode reativá-la explicitamente passando "LOGIN_DISABLED":
    # False no test_config, como faz test/test_rotas_auth/py
    app.config.setdefault(
        "LOGIN_DISABLED", app.config.get("TESTING", False)
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.models.transacao import Transacao
    from app.models.categoria import Categoria
    from app.models.emprestimo import Emprestimo
    from app.models.parcela import Parcela
    from app.models.usuario import Usuario

    # Importa o módulo apenas pelo efeito colateral de registrar
    # o user_loader. Usar "from app import security" (e não
    # "import app.security") evita sobrescrever a variável local
    # "app", que guarda a instância do Flask.
    from app import security # noqa: F401 - registra o user_loader
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(credito_bp)
    app.register_blueprint(debito_bp)
    app.register_blueprint(emprestimo_bp)

    @app.before_request
    def proteger_rotas():
        """
        Exige login em todas as rotas, exceto as do blueplint "auth" (login/logout) e as que
        não pertencem a nenhum blueprint (arquivos estátivos e rotas inexistentes).
        """

        if request.blueprint in (None, "auth"):
            return None

        return _verificar_login()

    @app.cli.command("criar-usuario")
    @click.argument("username")
    @click.password_option()
    def criar_usuario_command(username, password):
        """Cria o usuario único do sistema."""

        from app.services.auth_service import (
            UsuarioJaExisteError,
            criar_usuario,
        )

        try:
            criar_usuario(username, password)
            click.echo(f"Usuário '{username}' criado com sucesso.")
        except (ValueError, UsuarioJaExisteError) as erro:
            click.echo(f"Erro: {erro}")

    return app
