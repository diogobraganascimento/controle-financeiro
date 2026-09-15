"""
Entidade de domínio para categoria financeiras.
"""

class Categoria:
    """
    Representa uma categoria financeira no domínio da aplicação.
    
    Uma categoria classifa transações (ex: "Salário", "Aluguel") e está sempre associada a um tipo, para evitar ambiguidade entre categorias de crédito e de débito.
    """

    TIPOS_VALIDOS = ("credito", "debito")

    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo

    @property
    def nome(self) -> str:
        """Retorna o nome da categoria."""

        return self._nome

    @nome.setter
    def nome(self, nome: str):
        """Define o nome da categoria."""

        self._validar_nome(nome)
        self._nome = nome.strip()

    @property
    def tipo(self) -> str:
        """Retorna o tipo da categoria (credito ou debito)."""

        return self._tipo

    @tipo.setter
    def tipo(self, tipo: str):
        """Define o tipo da categoria."""

        self._validar_tipo(tipo)
        self._tipo = tipo

    def _validar_nome(self, nome: str):
        """Valida o nome da categoria."""

        if not isinstance(nome, str):
            raise TypeError(
                "O nome da categoria deve ser uma string."
            )

        if not nome.strip():
            raise ValueError(
                "O nome da categoria é obrigatório."
            )

    def _validar_tipo(self, tipo: str):
        """Valida o tipo da categoria."""

        if not isinstance(tipo, str):
            raise TypeError(
                "O tipo da categoria deve ser uma string."
            )

        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo de categoria inválido: {tipo}. "
                f"Valores aceitos: {self.TIPOS_VALIDOS}."
            )
