import sqlite3


def resetar_usuarios():
    # Conecta ao banco de dados
    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()

    try:
        # Apaga todos os usuários exceto o admin
        cursor.execute("DELETE FROM usuarios WHERE username != 'admin'")

        # Reseta o autoincremento, se não houver outros registros além do admin (SQLite usa sqlite_sequence)
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]

        if total == 1:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='usuarios'")

        # Confirma as alterações
        conn.commit()
        print("Usuários (exceto o admin) apagados e IDs resetados se aplicável.")

    except Exception as e:
        print("Error", e)
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    resetar_usuarios()
