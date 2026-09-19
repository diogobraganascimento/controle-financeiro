"""
Rotas para Débito, construídas a partir da fábrica de blueprint de transação.
"""

from app.domain.debito import Debito
from app.routes.transacao_routes import criar_blueprint_transacao

debito_bp = criar_blueprint_transacao(
    nome="debito",
    classe=Debito,
    tipo="debito",
    url_prefix="/debitos",
    template_dir="debitos",
)