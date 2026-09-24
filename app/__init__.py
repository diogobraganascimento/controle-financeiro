"""
Inicialização da aplicação Flask.
"""

from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes.home import home_bp
from app.routes.categoria import categoria_bp
from app.routes.credito import credito_bp
from app.routes.debito import debito_bp
from app.routes.emprestimo import emprestimo_bp


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

    db.init_app(app)

    from app.models.transacao import Transacao
    from app.models.categoria import Categoria
    from app.models.emprestimo import Emprestimo
    from app.models.parcela import Parcela
    

    app.register_blueprint(home_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(credito_bp)
    app.register_blueprint(debito_bp)
    app.register_blueprint(emprestimo_bp)

    return app
