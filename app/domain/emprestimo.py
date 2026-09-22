"""
Entidade de domínio para empréstimos.

Um empréstimo utiliza o Sistema Price de amortização: todas as
parcelas têm o mesmo valor, calculado a partir do valor retirado,
da taxa de juros mensal e da quantidade de parcelas.
"""

import calendar
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from app.domain.parcela import Parcela


def _somar_meses(data_base: date, meses: int) -> date:
    """
    Retorna a data resultante de somar uma quantidade de meses a uma data base, ajustando o dia caso o mês de destino tenha menos dias (ex: 31 de janeiro + 1 mês = 28/29 de fevereiro).
    """

    mes_total = data_base.month - 1 + meses
    ano = data_base.year + mes_total // 12
    mes = mes_total % 12 + 1

    ultimo_dia_do_mes = calendar.monthrange(ano, mes)[1]
    dia = min(data_base.day, ultimo_dia_do_mes)

    return date(ano, mes, dia)

class Emprestimo:
    """
    Representa um empréstimo no domínio da aplicação, calculado pelo Sistema Price(parcelas fixas).
    """

    def __init__(
        self,
        descricao: str,
        valor_retirado: Decimal,
        taxa_juros_mensal: Decimal,
        quantidade_parcelas: int,
        data_contratacao: date,
        parcelas: list[Parcela] | None = None,
        valor_parcela: Decimal | None = None,
        id: int | None = None,
    ):
        # id, parcelas e valor_parcela são opcionais: quando não
        # informados (criação de um empréstimo novo), são
        # calculados/gerados automaticamente. Quando informados
        # (reconstrução a partir do banco, via mapper), os valores
        # recebidos são usados como estão - preservando o estado
        # real das parcelas (quais já foram pagas).
        self.id = id
        self.descricao = descricao
        self.valor_retirado = valor_retirado
        self.taxa_juros_mensal = taxa_juros_mensal
        self.quantidade_parcelas = quantidade_parcelas
        self.data_contratacao = data_contratacao

        self.valor_parcela = (
            valor_parcela
            if valor_parcela is not None else self._calcular_valor_parcela()
        )
        self.parcelas = (
            parcelas if parcelas is not None else self._gerar_parcelas()
        )

    @property
    def descricao(self) -> str:
        """Retorna a descrição do empréstimo."""

        return self._descricao

    @descricao.setter
    def descricao(self, descricao: str):
        """Define a descrição do empréstimo."""

        if not isinstance(descricao, str):
            raise TypeError(
                "A descrição do empréstimo deve ser uma string."
            )

        if not descricao.strip():
            raise ValueError(
                "A descrição do empréstimo é obrigatória."
            )

        self._descricao = descricao.strip()

    @property
    def valor_retirado(self) -> Decimal:
        """Retorna o valor retirado do empréstimo"""

        return self._valor_retirado

    @valor_retirado.setter
    def valor_retirado(self, valor_retirado: Decimal):
        """Retorna o valor retirado do empréstimo."""

        if not isinstance(valor_retirado, Decimal):
            raise TypeError(
                "O valor retirado deve ser um Decimal."
            )

        if valor_retirado <= Decimal("0"):
            raise ValueError(
                "O valor retirado deve ser maior que zero."
            )

        self._valor_retirado = valor_retirado

    @property
    def taxa_juros_mensal(self) -> Decimal:
        """Retorna a taxa de juros mensal (em decimal, ex: 0.02)."""

        return self._taxa_juros_mensal

    @taxa_juros_mensal.setter
    def taxa_juros_mensal(self, taxa_juros_mensal: Decimal):
        """Define a taxa de juros mensal."""

        if not isinstance(taxa_juros_mensal, Decimal):
            raise TypeError(
                "A taxa de juros mensal deve ser um decimal."
            )

        if taxa_juros_mensal <= Decimal("0"):
            raise ValueError(
                "A taxa de juros mensal deve ser maior que zero."
            )

        self._taxa_juros_mensal = taxa_juros_mensal

    @property
    def quantidade_parcelas(self) -> int:
        """Retorna a quantidade de parcelas do empréstimo."""

        return self._quantidade_parcelas

    @quantidade_parcelas.setter
    def quantidade_parcelas(self, quantidade_parcelas: int):
        """Define a quantidade de parcelas do empréstimo."""

        if not isinstance(quantidade_parcelas, int):
            raise TypeError(
                "A quantidade de parcelas deve ser um inteiro."
            )

        if quantidade_parcelas <= 0:
            raise ValueError(
                "A quantidade de parcelas deve ser maior que zero."
            )

        self._quantidade_parcelas = quantidade_parcelas

    @property
    def data_contratacao(self) -> date:
        """Retorna a data de contratação do empréstimo."""

        return self._data_contratacao

    @data_contratacao.setter
    def data_contratacao(self, data_contratacao: date):
        """Define a data de contratação do empréstimo."""

        if not isinstance(data_contratacao, date):
            raise TypeError(
                "A data de contratação deve ser um objeto date."
            )

        self._data_contratacao = data_contratacao

    def _calcular_valor_parcela(self) -> Decimal:
        """
        Calcula p valor fixo da parcela pelo Sistema Price:
        
        parcela = valor_retirado * [i * (1+i)^n] / [(1+i)^n - 1]
        """

        i = self.taxa_juros_mensal
        n = self.quantidade_parcelas

        fator = (Decimal("1") + i) ** n

        parcela = self.valor_retirado * (i * fator) / (fator - Decimal("1"))

        return parcela.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _gerar_parcelas(self) -> list[Parcela]:
        """
        Gera a lista de parcelas do empréstimo, uma para cada mês, todas com o mesmo valor (Sistema Prica) e vencimento mensal a partir da data de contrução.
        """

        return [
            Parcela(
                numero=numero,
                valor=self.valor_parcela,
                data_vencimento=_somar_meses(
                    self.data_contratacao, numero
                ),
            )
            for numero in range(1, self.quantidade_parcelas + 1)
        ]

    @property
    def valor_final(self) -> Decimal:
        """
        Retorna o valor total a ser pago (soma de todas as parcelas).
        """

        return self.valor_parcela * self.quantidade_parcelas

    @property
    def juros_anual(self) -> Decimal:
        """
        Retorna a taxa de juros anual equivalente, calculada por juros compostos a partir da taxa mensal.
        """

        return (Decimal("1") + self.taxa_juros_mensal) ** 12 - Decimal("1")

    @property
    def parcelas_pagas(self) -> int:
        """Retorna a quantidade de parcelas já pagas."""

        return sum(1 for parcela in self.parcelas if parcela.paga)

    @property
    def parcelas_restantes(self) -> int:
        """Retorna a quantidade de parcelas ainda não pagas."""

        return self.quantidade_parcelas - self.parcelas_pagas

    @property
    def valor_restante(self) -> Decimal:
        """ReRetorna a soma do valor das parcelas ainda não pagas."""

        return sum(
            (parcela.valor for parcela in self.parcelas if not parcela.paga),
            start=Decimal("0"),
        )

    @property
    def situacao(self) -> str:
        """
        Retorna a situação do empréstimo: "quitado" se todas as parcelas estiveram pagas, "ativo" caso contrário.
        """

        return "quitado" if self.parcelas_restantes == 0 else "ativo"
