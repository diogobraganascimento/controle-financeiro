import sqlite3

import bcrypt
from flask import session
from datetime import datetime


def executar_consulta(query, parametros=(), fetchone=False, fetchall=False, commit=False):
    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()
    cursor.execute(query, parametros)

    resultado = None
    if fetchone:
        resultado = cursor.fetchone()
    elif fetchall:
        resultado = cursor.fetchall()

    if commit:
        conexao.commit()

    conexao.close()
    return resultado


def get_usuario_id():
    return session.get('usuario', {}).get('id')


def criar_senha_hash(senha):
    """Gera o hash da senha usando bcrypt."""
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def verificar_login(username, senha_digitada):
    """Verifica o login comparando a senha digitada com a hash no banco"""
    conn = sqlite3.connect("financeiro.db")
    cursor = conn.cursor()

    cursor.execute('SELECT senha_hash FROM usuarios WHERE username = ?', (username))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        senha_hash = resultado[0]
        senha_hash_bytes = senha_hash.encode('utf-8')
        senha_digitada_bytes = senha_digitada.encode('utf-8')

        if bcrypt.checkpw(senha_digitada_bytes, senha_hash_bytes):
            print('Login bem-sucedido!')
            return True
        else:
            print('Senha incorreta.')
            return False
    else:
        print('Usuário não encontrado.')
        return False


def validar_cpf(cpf: str) -> bool:
    """Valida o CPF (Cadastro de Pessoa Física)."""
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False

    return True


def validar_data(data_str: str) -> bool:
    """Valida se a string de data está no formato e representa uma data real."""
    try:
        datetime.strptime(data_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False
