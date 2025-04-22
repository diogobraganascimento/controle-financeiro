import sqlite3
from flask import session


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
