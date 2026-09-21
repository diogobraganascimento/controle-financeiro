"""
Entidade do domínio para parcelas de empréstimo.
"""

from datetime import date
from decimal import Decimal

class Parcela:
    """
    Representa uma parcela de um empréstimo.
    
    Uma percela sempre nasce como não paga (paga=False); ela é marcada como paga através do método pagar().
    """

    def __init__(
        self,
        numero: int,
        valor: Decimal,
        data_vencimento: date,
    ):
        self.numero = numero
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.paga = False

    @property
    def numero(self) -> int:
        """Retorna o número (posição) da parcela."""

        return self._numero

    @numero.setter
    def numero(self, numero: int):
        """Define o número da parcela."""
        if not isinstance(numero, int):
            raise TypeError(
                "O número da parcela deve ser um inteiro."
            )

        if numero <= 0:
            raise ValueError(
                "O número da parcela deve ser maior que zero."
            )

        self._numero = numero

    @property
    def valor(self) -> Decimal:
        """Retorna o valor da parcela."""

        return self._valor

    @valor.setter
    def valor(self, valor: Decimal):
        """Define o valor da parcela."""

        if not isinstance(valor, Decimal):
            raise TypeError(
                "O valor da parcela deve ser um Decimal."
            )

        if valor <= Decimal("0"):
            raise ValueError(
                "O valor da parcela deve ser maior que zero."
            )

        self._valor = valor

    @property
    def data_vencimento(self) -> date:
        """Retorna a data de vencimenot da parcela."""

        return self._data_vencimento

    @data_vencimento.setter
    def data_vencimento(self, data_vencimento: date):
        """Define a data de vencimento da parcela."""

        if not isinstance(data_vencimento, date):
            raise TypeError(
                "A data de vencimento deve ser um objeto date."
            )

        self._data_vencimento = data_vencimento

    def pagar(self):
        """
        Marca a parcela como paga.
        
        Não tem efeito se a parcela já estiver paga.
        """

        self.paga = True
