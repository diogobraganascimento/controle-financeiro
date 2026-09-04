""""
Ponto de entrada da aplicação Controle Financeiro.
"""

from app.config import Config


def main():
    """Inicializa a aplicação"""
    print(f"{Config.APP_NAME} iniciado!")


if __name__ == "__main__":
    main()
