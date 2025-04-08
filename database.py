import sqlite3


def criar_banco():
    """Cria as tabelas no banco de dados SQLite se não existirem."""
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()

    # Criar tabela de créditos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creditos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)

    # Criar tabela de débitos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',
            data_agendada TEXT
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_banco()
