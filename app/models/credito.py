"""
Modelo de Crédito.
"""


from datetime import date
from decimal import Decimal

from app.models.transacao import Transacao


class Credito(Transacao):
    """
    Representa uma entrada financeira no sistema.
    """

    def __init__(
        self,
        descricao: str,
        valor: Decimal,
        data: date,
        categoria: str,
        comprovante: str | None = None
    ):
        super().__init__(
            descricao = descricao,
            valor = valor,
            data = data,
            categoria = categoria,
            comprovante = comprovante,
        )
