"""
Modelo base para transações financeiras.
"""

from app.extensions import db


class Transacao(db.Model):
    """
    Representa uma transação financeira persistente no banco.
    """

    __tablename__ = "transacoes"

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    tipo = db.Column(
        db.String(20),
        nullable=False,
    )

    descricao = db.Column(
        db.String(200),
        nullable=False,
    )

    valor = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    data = db.Column(
        db.Date,
        nullable=False,
    )

    categoria = db.Column(
        db.String(100),
        nullable=False,
    )

    comprovante = db.Column(
        db.String(500),
        nullable=True,
    )