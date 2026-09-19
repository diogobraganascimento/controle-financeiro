"""
Rotas para Crédito, contruídas a partir da fábrica de blueprint de transação.
"""

from app.domain.credito import Credito
from app.routes.transacao_routes import criar_blueprint_transacao

credito_bp = criar_blueprint_transacao(
    nome="credito",
    classe=Credito,
    tipo="credito",
    url_prefix="/creditos",
    template_dir="creditos",
)