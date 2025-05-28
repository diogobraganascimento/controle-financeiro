import os
import sqlite3
import re
from datetime import datetime
from typing import Any, Optional, Tuple, Union
from flask import send_file
from io import BytesIO

import bcrypt
from flask import session
from werkzeug.utils import secure_filename


def executar_consulta(
        query: str,
        parametros: Union[Tuple, list] = (),
        fetchone: bool = False,
        fetchall: bool = False,
        commit: bool = False
) -> Optional[Union[Tuple, list]]:
    """
    Executa uma consulta SQL no banco de dados.

    Parâmetros:
        query (str): Consulta SQL a ser executada.
        parametros (tuple | list): Parâmetros da consulta.
        fetchone (bool): Se True, retorna um único resultado.
        fetchall (bool): Se True, retorna todos os resultados.
        commit (bool): Se True, confirma alterações no banco.

    Retorno:
        tuple | list | None: Resultado da consulta.
    """
    with sqlite3.connect('financeiro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute(query, parametros)

        resultado = None
        if fetchone:
            resultado = cursor.fetchone()
        elif fetchall:
            resultado = cursor.fetchall()

        if commit:
            conexao.commit()

    return resultado


def get_usuario_id() -> Optional[int]:
    """
    Retorna o ID do usuário logado.

    Retorno:
        int | None: ID do usuário ou None se não estiver logado.
    """
    return session.get('usuario', {}).get('id')


def criar_senha_hash(senha: str) -> bytes:
    """
    Gera o hash da senha usando bcrypt.

    Parâmetros:
        senha (str): Senha em texto puro.

    Retorno:
        bytes: Hash da senha.
    """
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())


def allowed_file(filename):
    """
    Verifica se a extensão do arquivo é permitida

    Parâmetros:
        filename (str): Nome do arquivo.

    Retorno:
        bool: True se permitido, False caso contrário.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def verificar_login(username: str, senha_digitada: str) -> bool:
    """
    Verifica o login comparando a senha digitada com a hash no banco

    Parâmetros:
        username (str): Nome de usuário.
        senha_digitada (str): Senha informada.

    Retorno:
        boll: True se login bem-sucedido, False caso contrário.
    """
    with sqlite3.connect("financeiro.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT senha_hash FROM usuarios WHERE usernme = ?', (username))
        resultado = cursor.fetchone()

    if resultado:
        senha_hash = resultado[0]
        if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash.encode('utf-8')):
            print('Login bem-sucedido!')
            return True
        else:
            print('Senha incorreta.')
    else:
        print('Usuário não encontrado.')

    return False


def validar_cpf(cpf: str) -> bool:
    """
    Valida o CPF (Cadastro de Pessoa Física).

    Parâmetros:
        cpf (str): CPF a ser validado.

    Retorno:
        bool: True se válido, False se inválido.
    """
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
    """
    Valida se a string representa uma data válida no formato DD-MM-YYYY.

    Parâmetros:
        data_str (str): Data como string.

    Retorno:
        bool: True se válido, False se inválido.
    """
    try:
        datetime.strptime(data_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def senha_segura(senha):
    """
    Valida se a senha é segura conforme regas estabelecidas.

    Parâmetros:
        senha (str): Senha a ser validada.

    Retorno:
        bool: True se segura, False caso contrário.
    """
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(regex, senha))


def salvar_arquivo_upload(file: Any, pasta_destino: str) -> Optional[str]:
    """
    Valida e salva um arquivo de upload na pasta destino.

    Parâmetro:
        file (FileStorage): Arquivo enviado.
        pasta_destino (str): Caminho da pasta destino.

    Retorno:
        str | None: Nome seguro do arquivo salvo ou None se invállido.
    """
    if file.filename == '':
        return None

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(pasta_destino, filename)
        file.save(filepath)
        return filename

    return None


def criar_tabela_usuarios():
    """
    Cria a tabela 'usuarios' no banco de dados, caso ela ainda não exista.

    Campos da tabela:
    - id: Identificador único do usuário (chave primária).
    - username: Nome de usuário, obrigatório e único.
    - senha_hash: Hash da senha do usuário, obrigatório.
    - is_admin: Indica se o usuário possui privilégios administrativos (BOOLEAN).
    - ativo: Indica se o usuário está ativo (BOOLEAN).
    - nome: Nome pessoal do usuário.
    - sobrenome: Sobrenome do usuário.
    - cpf: CPF do usuário.
    - nascimento: Data de nascimento do usuário.
    - cidade: Cidade do usuário.
    - estado: Estado do usuário.
    - celular: Número de celular do usuário.
    - email: Endereço de e-mail do usuário.
    - origem: Origem do contato do usuário.
    - canal: Canal de comunicação preferencial.
    - avatar: Caminho ou referência para o avatar do usuário.
    """
    query = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            ativo BOOLEAN DEFAULT 1,
            nome TEXT,
            sobrenome TEXT,
            cpf TEXT,
            nascimento TEXT,
            cidade TEXT,
            estado TEXT,
            celular TEXT,
            email TEXT,
            origem TEXT,
            canal TEXT,
            avatar TEXT
        )
    '''
    executar_consulta(query, commit=True)


def autenticar_usuario(username: str, senha: str) -> dict | None:
    """
    Autentica um usuário verificando o username e a senha fornecidos.

    Parâmetros:
        username (str): Nome do usuário.
        senha (str): Senha em texto puro.

    Retorno:
        dict | None: Dicionário com dados do usuário ('id', 'username', 'is_admin')
                     se a autenticação for bem-sucedida, ou None caso contrário.
    """
    query = "SELECT id, username, senha_hash, is_admin FROM usuarios WHERE username = ?"
    resultado = executar_consulta(query, (username,), fetchone=True)
    if resultado:
        id_usuario, username, senha_hash, is_admin = resultado
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            return {
                'id': id_usuario,
                'username': username,
                'is_admin': bool(is_admin)
            }
    return None


def desativar_usuario(id: int) -> None:
    """
    Desativa o usuário com o ID informado.

    Parâmetro:
        id (int): ID do usuário a ser desativado.

    Retorno:
        None
    """
    query = "UPDATE usuarios SET ativo = 0 WHERE id = ?"
    executar_consulta(query, (id,), commit=True)


def cadastrar_usuario(dados: dict) -> None:
    """
    Insere um novo usuário no banco de dados.

    Parâmetro:
        dados (dict): Dicionario contendo os dados do usuário.

    Retorno:
        None
    """
    query = """
        INSERT INTO usuarios (
            nome, sobrenome, cpf, nascimento, cidade, estado, celular,
            email, origem, canal, username, senha_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    parametros = (
        dados['nome'], dados['sobrenome'], dados['cpf'], dados['nascimento'],
        dados['cidade'], dados['estado'], dados['celular'], dados['email'],
        dados['origem'], dados['canal'], dados['username'], dados['senha_hash']
    )
    executar_consulta(query, parametros, commit=True)


def send_file_response(file_bytes_io: BytesIO, filename: str, mimetype: str):
    """
    Retorna uma resposta HTTP para download de arquivo

    Parâmetros:
        file_bytes_io (BytesIO): Objeto BytesIO com o conteúdo do arquivo.
        filename (str): Nome do arquivo para download.
        mimetype (str): Tipo MIME do arquivo (ex: 'application/pdf')

    Retorna:
        falsk.Response: Resposta para envio do arquivo.
    """
    file_bytes_io.seek(0)
    return send_file(
        file_bytes_io,
        download_name=filename,
        as_attachment=True,
        mimetype=mimetype
    )
