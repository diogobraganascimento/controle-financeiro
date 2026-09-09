"""
Inicialização da aplicação Flask.
"""

from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes.home import home_bp


def create_app():
    """
    Cria e configura uma instancia da aplicação Flask.

    returns:
        Flask: aplicação Flask configurada.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.models.transacao import Transacao

    app.register_blueprint(home_bp)

    return app
