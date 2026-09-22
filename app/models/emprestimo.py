"""
Modelo de persistência para empréstimo.
"""

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.parcela import Parcela

class Emprestimo(db.Model):
    """
    Modelo SQLAlchemy da tabela "emprestimos"
    """

    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    descricao: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    valor_retirado: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    taxa_juros_mensal: Mapped[Decimal] = mapped_column(
        Numeric(10, 6),
        nullable=False,
    )

    quantidade_parcelas: Mapped[int] = mapped_column(
        nullable=False,
    )

    data_contratacao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    valor_parcela: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    # Um empréstimo tem muitas parcelas. Excluir o empréstimo
    # excluir automaticamente todas as suas parcelas (cascade),
    # evitando parcelas "orfãs" apontando para um empréstimo
    # inexistente

    parcelas: Mapped[list["Parcela"]] = relationship(
        back_populates="emprestimo",
        cascade="all, delete-orphan",
        order_by="Parcela.numero",
    )
