"""
Inicialização da aplicação Flask.
"""


from flask import Flask, render_template

from app.config import Config
from app.routes.home import home_bp


def create_app():
    """
    Cria e configura uma instancia da aplicação Flask.

    returns:
        Flask: aplicação Flask configurada.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(home_bp)

    return app
