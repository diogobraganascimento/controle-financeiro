"""
Configurações da aplicação.
"""

import os


class Config:
    """Configurações básicas da aplicação."""

    APP_NAME = "Controle Financeiro"

    BASE_DIR = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__))
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(BASE_DIR, "controle_financeiro.sqlite3")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
