"""
Entidade de domínio para transações financeiras.
"""

from datetime import date
from decimal import Decimal


class Transacao:
    """
    Representa uma transação financeira no domínio da aplicação.
    """

    def __init__(
        self,
        descricao: str,
        valor: Decimal,
        data: date,
        categoria: str,
        comprovante: str | None = None,
    ):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        self.comprovante = comprovante

    @property
    def descricao(self) -> str:
        """Retorna a descrição da transação."""

        return self._descricao

    @descricao.setter
    def descricao(self, descricao: str):
        """Define a descrição da transação."""

        self._validar_descricao(descricao)

        self._descricao = descricao.strip()

    @property
    def valor(self) -> Decimal:
        """Retorna o valor da transação."""

        return self._valor

    @valor.setter
    def valor(self, valor: Decimal):
        """Define o valor da transação."""

        self._validar_valor(valor)

        self._valor = valor

    @property
    def data(self) -> date:
        """Retorna a data da transação."""

        return self._data

    @data.setter
    def data(self, data: date):
        """Define a data da transação."""

        self._validar_data(data)

        self._data = data

    @property
    def categoria(self) -> str:
        """Retorna a categoria da transação."""

        return self._categoria

    @categoria.setter
    def categoria(self, categoria: str):
        """Define a categoria da transação."""

        self._validar_categoria(categoria)

        self._categoria = categoria.strip()

    @property
    def comprovante(self) -> str | None:
        """Retorna o comprovante da transação."""

        return self._comprovante

    @comprovante.setter
    def comprovante(self, comprovante: str | None):
        """Define o comprovante da transação."""

        if comprovante is not None and not isinstance(
            comprovante,
            str,
        ):
            raise TypeError(
                "O comprovante deve ser uma string ou None."
            )

        self._comprovante = comprovante

    def impacto_saldo(self) -> Decimal:
        """
        Retorna o impacto da transação no saldo.

        As subclasses devem implementar este comportamento.
        """

        raise NotImplementedError(
            "As subclasses devem implementar impacto_saldo()."
        )

    def _validar_descricao(self, descricao: str):
        """Valida a descrição da transação."""

        if not isinstance(descricao, str):
            raise TypeError(
                "A descrição da transação deve ser uma string."
            )

        if not descricao.strip():
            raise ValueError(
                "A descrição da transação é obrigatória."
            )

    def _validar_valor(self, valor: Decimal):
        """Valida o valor da transação."""

        if not isinstance(valor, Decimal):
            raise TypeError(
                "O valor da transação deve ser um Decimal."
            )

        if valor <= Decimal("0"):
            raise ValueError(
                "O valor da transação deve ser maior que zero."
            )

    def _validar_data(self, data: date):
        """Valida a data da transação."""

        if not isinstance(data, date):
            raise TypeError(
                "A data da transação deve ser um objeto date."
            )

    def _validar_categoria(self, categoria: str):
        """Valida a categoria da transação."""

        if not isinstance(categoria, str):
            raise TypeError(
                "A categoria da transação deve ser uma string."
            )

        if not categoria.strip():
            raise ValueError(
                "A categoria da transação é obrigatória."
            )
        