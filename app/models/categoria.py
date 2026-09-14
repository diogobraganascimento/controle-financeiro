"""
Modelo de persistência para categoria financeiras.
"""

from sqlalchemy import CheckConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Categoria(db.Model):
    """
    Modelo SQLAlchemy da tabela "categorias".
    """

    __tablename__ = "categorias"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('credito', 'debito')",
            name="ck_categorias_tipo",
        ),
        UniqueConstraint(
            "nome",
            "tipo",
            name="uq_categorias_nome_tipo",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )