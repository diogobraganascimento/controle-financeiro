"""
Modelo de persistência para o usuário do sistema.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Usuario(db.Model):
    """
    Modelo SQLAlchemy da tabela "usuarios".
    """

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
