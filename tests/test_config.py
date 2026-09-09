"""
Testes das configurações da aplicação.
"""

from app import create_app

def test_aplicacao_deve_usar_sqlite():
    """
    Verifica se a aplicação está configurada para usar SQLite.
    """

    app = create_app()

    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith(
        "sqlite:///"
    )

def test_aplicacao_deve_desativar_track_modifications():
    """
    Verifica se o rastreamento de modificações está desativado.
    """

    app = create_app()

    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False