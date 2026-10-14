"""
Entidade de domínio para recorrências financeiras.

Uma recorrência é um "molde" de transação mensal (ex: salário
todo dia 5, aluguel todo dia 10). Ela não é uma transação em si:
seu papel é calcular quais ocorrências ainda não foram geradas
como transações reais (Credito/Debito), evitando duplicatas
através do rastreamento de `ultima_geracao`.
"""

import calendar
from datetime import date
from decimal import Decimal


def _data_no_mes(ano: int, mes: int, dia: int) -> date:
    """
    Retorna a data correspondente ao dia pedido, dentro do mês e
    ano informados, ajustando para o último dia do mês caso o dia
    pedido não exista nele (ex: dia 31 em fevereiro).
    """

    ultimo_dia_do_mes = calendar.monthrange(ano, mes)[1]

    return date(ano, mes, min(dia, ultimo_dia_do_mes))


class Recorrencia:
    """
    Representa uma recorrência financeira mensal no domínio da aplicação.
    """

    TIPOS_VALIDOS = ("credito", "debito")

    def __init__(
        self,
        descricao: str,
        valor: Decimal,
        categoria: str,
        tipo: str,
        dia_do_mes: int,
        data_inicio: date,
        data_fim: date | None = None,
        ultima_geracao: date | None = None,
        ativa: bool = True,
        id: int | None = None,
    ):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria
        self.tipo = tipo
        self.dia_do_mes = dia_do_mes
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.ultima_geracao = ultima_geracao
        self.ativa = ativa

    @property
    def descricao(self) -> str:
        """Retorna a descrição da recorrência."""

        return self._descricao

    @descricao.setter
    def descricao(self, descricao: str):
        """Define a descrição da recorrência."""

        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser uma string.")
        
        if not descricao.strip():
            raise ValueError("A descrição é obrigatória.")

        self._descricao = descricao.strip()

    @property
    def valor(self) -> Decimal:
        """Retorna o valor da recorreência."""

        return self._valor

    @valor.setter
    def valor(self, valor: Decimal):
        """Define o valor da recorrência."""

        if not isinstance(valor, Decimal):
            raise TypeError("O valor deve ser um Decimal.")

        if valor <= Decimal("0"):
            raise ValueError("O valor deve ser maior que zero.")

        self._valor = valor

    @property
    def categoria(self) -> str:
        """Retorna a categoria da recorrência."""

        return self._categoria

    @categoria.setter
    def categoria(self, categoria: str):
        """Define a categoria da recorrência."""

        if not isinstance(categoria, str):
            raise TypeError("A categoria deve ser uma string.")

        if not categoria.strip():
            raise ValueError("A categoria é obrigatória.")

        self._categoria = categoria.strip()

    @property
    def tipo(self) -> str:
        """Retorna o tipo da recorrência (credito ou debito)."""

        return self._tipo

    @tipo.setter
    def tipo(self, tipo: str):
        """Define o tipo da recorrência."""

        if not isinstance(tipo, str):
            raise TypeError("O tipo deve ser uma setring.")

        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo de recorrência inválido: {tipo}."
                f"Valores aceitos: {self.TIPOS_VALIDOS}."
            )

        self._tipo = tipo
        
