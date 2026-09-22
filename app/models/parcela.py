"""
Modelo de persitência para parcelas de empréstimo.
"""

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

if TYPE_CHECKING:
    from app.models.emprestimo import Emprestimo

class Parcela(db.Model):
    """
    Modelo SQLAlchemy da tabela "parcela". 
    """

    __tablename__ = "parcelas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    emprestimo_id: Mapped[int] = mapped_column(
        ForeignKey("emprestimos.id"),
        nullable=False,
    )

    numero: Mapped[int] = mapped_column(
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    data_vencimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    paga: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    emprestimo: Mapped["Emprestimo"] = relationship(
        back_populates="parcelas",
    )
