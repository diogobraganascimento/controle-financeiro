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

    # Usada pelo Flask para assinar o cookie de sessão (login).
    # Em desenvolvimento, um valor fixo é aceitável; antes de qualquer deploy, isso deve vir de uma variável
    # de ambiente secreta, nunca ficar hardcoded no código-fonte.
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "chave-de-desenvolvimento-trocar-antes-do-deploy"
    )
