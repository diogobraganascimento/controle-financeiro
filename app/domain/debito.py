"""
Entidade de domínio para débitos.
"""

from datetime import date
from decimal import Decimal

from app.domain.transacao import Transacao


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
        id: int | None = None,
    ):
        super().__init__(
            descricao=descricao,
            valor=valor,
            data=data,
            categoria=categoria,
            comprovante=comprovante,
            id=id,
        )

    def impacto_saldo(self) -> Decimal:
        """
        Retorna o impacto negativo do débito no saldo.
        """

        return -self.valor

    @property
    def tipo(self) -> str:
        """
        Retorna o tipo da transação.
        """

        return "debito"
    