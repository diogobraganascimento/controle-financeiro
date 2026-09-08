"""
Modelo de Débito.
"""

from datetime import date
from decimal import Decimal

from app.models.transacao import Transacao


class Debito(Transacao):
    """
    Representa uma saída financeira.
    """

    def __init__(
        self,
        descricao: str,
        valor: Decimal,
        data: date,
        categoria: str,
        comprovante: str | None = None,
    ):
        super().__init__(
            descricao=descricao,
            valor=valor,
            data=data,
            categoria=categoria,
            comprovante=comprovante,
        )