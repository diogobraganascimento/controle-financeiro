import sqlite3
import bcrypt

def criar_usuario_admin():
    usuario = "admin"
    senha = "admin123"  # você pode alterar essa senha depois
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (username, senha_hash, is_admin) VALUES (?, ?, ?)",
                       (usuario, senha_hash, True))
        conexao.commit()
        print("Usuário administrador criado com sucesso.")
    except sqlite3.IntegrityError:
        print("Usuário já existe.")
    finally:
        conexao.close()

if __name__ == "__main__":
    criar_usuario_admin()
