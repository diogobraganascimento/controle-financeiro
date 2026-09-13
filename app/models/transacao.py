"""
Modelo base para transações financeiras.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Transacao(db.Model):
    """
    Representa uma transação financeira persistente no banco.
    """

    __tablename__ = "transacoes"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('credito', 'debito')",
            name="ck_transacoes_tipo",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    descricao: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    data: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    comprovante: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
