import os
import sqlite3
import bcrypt
import json
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash

import pandas as pd
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from utils import (
    executar_consulta,
    get_usuario_id,
    criar_senha_hash,
    allowed_file,
    verificar_login,
    validar_cpf,
    validar_data,
    senha_segura,
    salvar_arquivo_upload,
    criar_tabela_usuarios,
    autenticar_usuario,
    desativar_usuario,
    cadastrar_usuario,
    send_file_response,
)

app = Flask(__name__)
app.secret_key = 'Q1w2e3r4t5'

google_bp = make_google_blueprint(
    client_id="511880856381-oj0hr6l9doa644ndlmsdls6u6jgdhk6k.apps.googleusercontent.com",
    client_secret="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",
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)

github_bp = make_github_blueprint(
    client_id="Ov23liowgLsKjMG17f8g",
    client_secret="f1d6f82f65a12bcb80f22407faed255e2e425a2a",
    redirect_url="http://localhost:5000/login/github/authorized",
)

app.register_blueprint(google_bp, url_prefix="/login")  # Google
app.register_blueprint(github_bp, url_prefix="/login")  # GitHub


criar_tabela_usuarios()


# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para exibir e processar o formulário de login do usuário.
    """
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        usuario_logado = autenticar_usuario(usuario, senha)
        if usuario_logado:
            session['usuario'] = {
                'id': usuario_logado['id'],
                'username': usuario_logado['username']
            }
            session['is_admin'] = usuario_logado['is_admin']

            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))

        flash("Usuário ou senha inválidos", "danger")

    return render_template('login.html')


# Rota de Logon/google
@app.route("/login/google", endpoint="login_google")
def login_google():
    """
    Rota de login via Google OAuth.

    Redireciona o usuário para o fluxo de autenticação do Google se não estiver autorizado.
    Após autenticação, obtém e exibe o nome e email do usuário autenticado.

    Retorno:
        Response: Redireciona para o login do Google ou exibe mensagem de boas-vindas.
    """
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Erro ao acessar dados do Google", 400

    dados = resp.json()
    email = dados["email"]
    nome = dados.get("name", "Usuário")

    return f"Bem-vindo(a), {nome} ({email})"


# Rota de Logon/Github
@app.route("/login/github", endpoint="login_github")
def login_github():
    """
    Rota de login via GitHub OAuth.

    Redireciona o usuário para o fluxo de autenticação do GitHub se não estiver autorizado.
    Após autenticação, obtém e exibe o nome e email do usuário autenticado.

    Retorno:
        Response: Redireciona para o login do GitHub ou exibe mensagem de boas-vindas.
    """
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    if not resp.ok:
        return "Erro ao acessar GitHub", 400

    dados = resp.json()
    nome = dados.get("name") or dados.get("login")
    email = dados.get("email", "E-mail não disponível")

    return f"Bem-vindo(a), {nome} ({email})"


# Rota do Perfil
@app.route('/perfil')
def perfil():
    """
    Rota para exibição do perfil do usuário autenticado.

    Verifica se o usuário está logado e, se estiver, busca as informações completas
    do perfil no banco de dados, renderizando a página de perfil.

    Returns:
        Response: Redireciona para o login se não autenticado ou exibe o perfil.
    """
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar o perfil.', 'warning')
        return redirect(url_for('login'))

    usuario_nome = session['usuario']['username']

    query = """
        SELECT id, username, is_admin, 
                ativo, nome, sobrenome, 
                cpf, nascimento, cidade, 
                estado, celular, email, 
                origem, canal
        FROM usuarios
        WHERE username = ?
    """
    resultado = executar_consulta(query, (usuario_nome,), fetchone=True)

    if resultado:
        # Mapeando o resultado para um dicionário com nomes das colunas
        campos = [
            'id', 'username', 'admin', 'ativo',
            'nome', 'sobrenome', 'cpf', 'nascimento',
            'cidade', 'estado', 'celular', 'email',
            'origem', 'canal'
        ]
        usuario = dict(zip(campos, resultado))
    else:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('login'))

    return render_template('perfil.html', usuario=usuario)


@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    """
    Rota para upload de avatar do usuário.

    Valida o arquivo enviado, salva na pasta avatares e atualiza o caminho no banco de dados.
    Atualiza também a sessão do usuário para refletir a nova imagem.

    Retorno:
        Response: Redireciona para a página de perfil com mensagem de sucesso ou erro.
    """
    file = request.files.get('avatar')

    if not file:
        flash('Nenhum arquivo enviado.')
        return redirect(url_for('perfil'))

    pasta_destino = os.path.join(app.root_path, 'static', 'avatars')
    filename = salvar_arquivo_upload(file, pasta_destino)

    if filename:
        # Atualiza avatar no banco de dados
        conn = sqlite3.connect('financeiro.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET avatar = ? WHERE id = ?',
            (filename, session['usuario']['id'])
        )
        conn.commit()
        conn.close()

        # Atualiza avatar na sessão
        session['usuario']['avatar'] = filename

        flash('Avatar atualizado com sucesso!')
    else:
        flash('Avatar não permitido ou inválido.')

    return redirect(url_for('perfil'))


# Rota de Desativação da Conta
@app.route('/desativar_conta/<int:id>', methods=['POST'])
def desativar_conta(id):
    """
    Rota para desativar a conta de um usuário.

    Desativa o usuário no banco dedados, limpando a sessão e redirecionando para a página de boas-vindas.

    Parâmetro:
        id (int): ID do usuário a ser desativado.

    Retorno:
        Response: Redireciona para a rota 'welcome' com a mensagem de sucesso.
    """
    if 'usuario' not in session:
        flash('Você precisa estar logado para fazer isso.', 'danger')
        return redirect(url_for('login'))

    desativar_usuario(id)

    session.clear()
    flash('Conta desativada com sucesso.', 'success')
    return redirect(url_for('welcome'))


# Roda de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Rota para cadastro de novos usuários.

    Exibe o formulário de cadastro e processa os dados enviados, realizando validações.
    Se tudo estiver correto, insere o usuário no banco de dados e redireciona para o login.

    Retorno:
        Response: Redireciona para a rota de login ou recarrega a página de cadatro.
    """
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        cpf = request.form.get('cpf')
        nascimento = request.form.get('data_nascimento')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        celular = request.form.get('celular')
        email = request.form.get('email')
        origem = request.form.get('como_conheceu')
        canal = request.form.get('canal_preferido')
        username = email.split('@')[0]
        senha = request.form.get('password')
        confirmar_senha = request.form.get('confirm_password')
        termos = request.form.get('termos')

        if not validar_cpf(cpf):
            flash("CPF inválido.", "danger")
            return redirect(url_for('cadastro'))

        if not validar_data(nascimento):
            flash("Data de nascimento inválida. Use o formato DD-MM-YYYY.", "danger")
            return redirect(url_for('cadastro'))

        if not all([nome, sobrenome, email, senha, confirmar_senha]):
            flash("Por favor, preencha todos os campos obrigatórios.", "danger")
            return redirect(url_for('cadastro'))

        if not senha_segura(senha):
            flash("A senha deve conter no mínimo 8 caracteres, incluindo:"
                  "1 letra maiúscula"
                  "1 letra minúscula"
                  "1 número"
                  "1 carácter especial", "danger")
            return redirect(url_for('cadastro'))

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for('cadastro'))

        if termos != 'on':
            flash("Você precisa aceitar os termos de uso.", "warning")
            return redirect(url_for('cadastro'))

        senha_hash = criar_senha_hash(senha)

        dados = {
            'nome': nome,
            'sobrenome': sobrenome,
            'cpf': cpf,
            'nascimento': nascimento,
            'cidade': cidade,
            'estado': estado,
            'celular': celular,
            'email': email,
            'origem': origem,
            'canal': canal,
            'username': username,
            'senha_hash': senha_hash
        }

        try:
            cadastrar_usuario(dados)
            flash("Cadastro realizado com sucesse! Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Usuário ou e-mail já cadastrado.", "warning")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')


# Rota de Logout
@app.route('/logout')
def logout():
    """
    Realiza o logout do usuário, encerrando a sessão.

    Remove os dados do usuário da sessão, exibe uma mensagem de sucesso
    e redireciona para a página de boas-vindas.
    """
    session.pop('usuario', None)
    flash("Você saiu com sucesso", "success")
    return redirect(url_for('welcome'))


# Rota do Welcome
@app.route('/')
def welcome():
    """
    Exibe a página de boas-vindas.

    Renderiza o template 'welcome.html', que serve como página inicial ou
    de boas-vindas para os usuários.
    """
    return render_template("welcome.html")


# Rota Home
@app.route("/home", methods=["GET"])
def home():
    """
    Exibe a página principal (Home) com dados financeiros do usuário.

    Requisitos:
        - Usuário autenticado (verificação via get_usuario_id)

    Funcionalidades:
        - Filtra débitos por status, data e busca por descrição.
        - Calcula totais e categorias de créditos e débitos.
        - Prepara dados para gráficos (Chart.js).
        - Renderiza o template 'home.html' com todas as informações.

    Parâmetros:
        - status (str): Filtro de status do débito ('Pago', 'Pendente', etc.).
        - data (str): Filtro por tipo de data ('agendada', 'paga').
        - busca (str): Filtro textual na descrição de débito.

    Retorno:
        - Template renderizado 'home.html'
    """
    usuario_id = get_usuario_id()
    if not usuario_id:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    # Filtros
    status_filtro = request.args.get("status")
    data_filtro = request.args.get("data")
    busca = request.args.get("busca", "").lower()

    query = "SELECT * FROM debitos WHERE usuario_id = ?"
    params = [usuario_id]

    if status_filtro:
        query += " AND status = ?"
        params.append(status_filtro)

    if data_filtro == "agendada":
        query += " AND data_agendada IS NOT NULL"
    elif data_filtro == "paga":
        query += " AND status = 'Pago'"

    tabela_debitos = executar_consulta(query, params, fetchall=True)

    # Aplica filtro de busca por descrição (índice 2 = descrição)
    if busca:
        tabela_debitos = [debito for debito in tabela_debitos if busca in debito[2].lower()]

    # Créditos (somente do usuário)
    creditos = executar_consulta(
        "SELECT categoria, SUM(valor) FROM creditos WHERE usuario_id = ? GROUP BY categoria",
        (usuario_id,),
        fetchall=True
    )
    total_creditos = sum([row[1] for row in creditos])

    # Débitos (somente do usuário)
    debitos = executar_consulta(
        "SELECT categoria, SUM(valor) FROM debitos WHERE usuario_id = ? GROUP BY categoria",
        (usuario_id,),
        fetchall=True
    )
    total_debitos = sum([row[1] for row in debitos])

    # Preparação para Chart.js
    dados_creditos = {
        "labels": [c[0] for c in creditos],
        "valores": [c[1] for c in creditos]
    }

    dados_debitos = {
        "labels": [d[0] for d in debitos],
        "valores": [d[1] for d in debitos]
    }

    conexao.close()

    return render_template("home.html",
                           creditos=creditos,
                           debitos=debitos,
                           total_creditos=total_creditos,
                           total_debitos=total_debitos,
                           tabela_debitos=tabela_debitos,
                           dados_debitos=dados_debitos,
                           dados_creditos=dados_creditos)


# Rota Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    """
    Exibe o painel de administração.

    Requisito:
        - O usuário deve estar autenticado como administrador (session['is_admin']).

    Funcionalidades:
        - Verifica se o usuário possui permissão de administrador.
        - Redireciona para a página de login se não for administrador.
        - Renderiza o template 'admin/dashboard.html' para administradores.

    Retorno:
        - Template renderizado 'admin/dashboard.html' para administradores.
        - Redireciona para o 'login' se não autorizado.
    """
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')


# Rota para a página de crédito e salvar dados
@app.route("/credito", methods=["GET", "POST"])
def credito():
    """
    Gerencia o cadastro e a visualização de créditos do usuário logado.

    Funcionalidade:
        - Verifica se o usuário está logado.
        - No método POST:
            - Obtém os dados do formulário.
            - Insere o novo crédito no banco de dados, se todos os campos estiverem preenchidos.
            - Exibe mensagem de sucesso e redireciona para a mesma página.

        - No método GET:
            - Recupera e exibe todos os créditos do usuário logado.

    Requisitos:
        - O usuário deve estar autenticado (session['usuario']).

    Retorno:
        - Renderiza o template 'credito.html' com a lista de crédito do usuário.
        - Redireciona para 'login' se o usuário não estiver autenticado.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario']['id']

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            query = """
                INSERT INTO creditos (valor, descricao, tipo, categoria, data, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            parametros = (valor, descricao, tipo, categoria, data, usuario_id)
            executar_consulta(query, parametros, commit=True)
            flash("Crédito cadastrado com sucesso!", "success")
            return redirect(url_for('credito'))

    # Buscar registros apenas do usuário logado
    query_creditos = "SELECT * FROM creditos WHERE usuario_id = ?"
    creditos = executar_consulta(query_creditos, (usuario_id,), fetchall=True)

    return render_template("credito.html", creditos=creditos)


# Rota para página de débito e salvar dados
@app.route("/debito", methods=["GET", "POST"])
def debito():
    """
    Gerencia o cadastro e a visualização de débitos do usuário logado.

    Funcionalidades:
        - Verifica se o usuário está logado.
        - No método POST:
            - Obtém os dados do formulário.
            - Insere o novo débito no banco de dados, se todos os campos estiverem preenchidos.
            - Exibe mensagem de sucesso.
        - No método GET:
            - Recupera e exibe todos os débitos do usuário logado.

    Requisitos:
        - O usuário deve estar autenticado (session['usuario']).

    Retorno:
        - Renderiza o template 'debito.html' com a lista de débitos do usuário.
        - Redireciona para 'login' se o usuário não estiver autenticado.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario']['id']

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            query = """
                INSERT INTO debitos (valor, descricao, tipo, categoria, data, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            parametros = (valor, descricao, tipo, categoria, data, usuario_id)
            executar_consulta(query, parametros, commit=True)
            flash("Débito cadastrado com sucesso!", "success")

    # Buscar todos os registros da tabela de crédito
    query_debitos = "SELECT * FROM debitos WHERE usuario_id = ?"
    debitos = executar_consulta(query_debitos, (usuario_id,), fetchall=True)

    return render_template("debito.html", debitos=debitos)


# Rota para a página About
@app.route("/about")
def about():
    """
    Renderiza a página 'Sobre' do sistema.

    Funcionalidade:
        - Exibe informações institucionais ou descritivas sobre o sistema.

    Requisitos:
        - Nenhum requisito de autenticação.

    Retorno:
        - Renderiza o template 'about.html'.
    """
    return render_template("about.html")


# Rota para editar dados da tabela de crédito
@app.route("/editar_credito/<int:id>", methods=["GET", "POST"])
def editar_credito(id):
    """
    Edita um crédito existente no sistema.

    Parâmetro:
        id (int): ID do crédito a ser editado.

    Funcionalidade:
        - GET: Recupera os dados do crédito para exibir no formulário de edição.
        - POST: Atualiza o crédito com os dados informados pelo usuário.

    Requisitos:
        - O usuário deve estar autenticado (não implementado na função).

    Retorno:
        - GET: Renderiza o template 'editar_credito.html' com os dados do crédito.
        - POST: Redireciona para a página de créditos após a atualização.
    """
    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        query = """
            UPDATE creditos
            SET valor = ?, descricao = ?, tipo = ?, categoria = ?, data = ?
            WHERE id = ?
        """

        parametros = (valor, descricao, tipo, categoria, data, id)
        executar_consulta(query, parametros, commit=True)
        return redirect(url_for("credito"))

    query = "SELECT * FROM creditos WHERE id = ?"
    credito = executar_consulta(query, (id,), fetchone=True)

    return render_template("editar_credito.html", credito=credito)


# Rota para editar dados da tabela de débito
@app.route("/editar_debito/<int:id>", methods=["GET", "POST"])
def editar_debito(id):
    """
    Edita um débito existente no sistema.

    Parâmetro:
        id (int): ID do débito a ser editado.

    Funcionalidade:
        - GET: Recupera os dados do débito para exibir no formulário de edição.
        - POST: Atualiza o débito com os dados informados pelo usuário.

    Requisitos:
        - O usuário deve estar autenticado (não implementado na função).

    Retorno:
        - GET: Renderiza o template 'editar_debito.html' com os dados do débito.
        - POST: Redireciona para a página de débitos após a atualização.
    """
    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        query = """
            UPDATE debitos
            SET valor = ?, descricao = ?, tipo = ?, categoria = ?, data = ?
            WHERE id = ?
        """
        parametros = (valor, descricao, tipo, categoria, data, id)
        executar_consulta(query, parametros, commit=True)
        return redirect(url_for("debito"))

    query = "SELECT * FROM debitos WHERE id  = ?"
    debito = executar_consulta(query, (id,), fetchone=True)

    return render_template("editar_debito.html", debito=debito)


# Rota para excluir dados da tabela crédito
@app.route("/excluir_credito/<int:id>")
def excluir_credito(id):
    """
    Exclui um crédito do sistema com base no ID.

    Parâmetro:
        id (int): ID do crédito a ser excluído.

    Funcionalidade:
        - Verifica se o usuário está autenticado.
        - Exclui o registro de crédito correspondente ao ID.
        - Redireciona para a página de créditos.

    Requisitos:
        - O usuário deve estar autenticado.

    Retorno:
        - Redireciona para a rota 'credito' após a exclusão.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    query = "DELETE FROM creditos WHERE id = ?"
    executar_consulta(query, (id,), commit=True)
    return redirect(url_for("credito"))


# Rota para excluir dados da tabela débito
@app.route("/excluir_debito/<int:id>")
def excluir_debito(id):
    """
    Exclui um débito do sistema com base no ID.

    Parâmetro:
        id (int): ID do débito a ser excluído.

    Funcionalidade:
        - Verifica se o usuário está autenticado.
        - Exclui o registro de débito correspondente ao ID.
        - Redireciona para a página de débitos.

    Requisitos:
        - O usuário deve estar autenticado.

    Retorno:
        - Redireciona para a rota 'debito' após a exclusão.
    """
    if 'usuario' not in session:
        return redirect(url_for('login'))

    query = "DELETE FROM debitos WHERE id = ?"
    executar_consulta(query, (id,), commit=True)
    return redirect(url_for("debito"))


# Rota para atualizar o status do débito
@app.route('/atualizar-status-debito/<int:id>', methods=['POST'])
def atualizar_status_debito(id):
    """
    Atualiza o status de um débito e, se necessário, define a data agendada.

    Parâmetro:
        id (int): ID do débito a ser atualizado.

    Funcionalidade:
        - Obtém o novo status do formulário.
        - Se o status for 'Agendado' e a data estiver presente, atualiza ambos.
        - Caso contrário, atualiza apenas o status e remove a data agendada.
        - Redireciona para a página de débitos.

    Requisitos:
        - A requisição deve ser do tipo POST.

    Retorno:
        - Redireciona para a rota 'debito' após a atualização.
    """
    status = request.form.get('status')
    data_agendada = request.form.get('data_agendada', None)

    if status == 'Agendado' and data_agendada:
        query = "UPDATE debitos SET status = ?, data_agendada = ? WHERE id = ?"
        parametros = (status, data_agendada, id)
    else:
        query = "UPDATE debitos SET status = ?, data_agendada = NULL WHERE id = ?"
        parametros = (status, id)

    executar_consulta(query, parametros, commit=True)
    return redirect(url_for('debito'))


# Rota para exportação dados em formatos PDF, JSON e XLS
@app.route('/exportar/<formato>')
def exportar_dados(formato):
    """
    Exporta os dados financeiros (créditos e débitos) em diferentes formatos.

    Parâmetro:
        formato (str): Formato de exportação. Aceita 'xls', 'json' ou 'pdf'.

    Retorno:
        - Arquivo gerado para download no formato solicitado.
        - Em caso de formato inválido, retorna status 400 com mensagem.
    """
    with sqlite3.connect('financeiro.db') as conexao:
        df_creditos = pd.read_sql_query("SELECT * FROM creditos", conexao)
        df_debitos = pd.read_sql_query("SELECT * FROM debitos", conexao)

    if formato == 'xls':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_creditos.to_excel(writer, sheet_name='Créditos', index=False)
            df_debitos.to_excel(writer, sheet_name='Débitos', index=False)
        return send_file_response(output, 'dados_financeiros.xlsx',
                                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    elif formato == 'json':
        dados = {
            "creditos": df_creditos.to_dict(orient="records"),
            "debitos": df_debitos.to_dict(orient="records")
        }
        output = BytesIO()
        output.write(json.dumps(dados, indent=4).encode('utf-8'))
        return send_file_response(output, 'dados_financeiros.json', 'application/json')

    elif formato == 'pdf':
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "Relatório de Créditos", ln=True, align="C")
        for _, row in df_creditos.iterrows():
            pdf.multi_cell(0, 10, txt=str(row.to_dict()))

        pdf.add_page()
        pdf.cell(200, 10, "Relatório de Débitos", ln=True, align="C")
        for _, row in df_debitos.iterrows():
            pdf.multi_cell(0, 10, txt=str(row.to_dict()))

        output_bytes = pdf.output(dest='S').encode('latin-1')
        output = BytesIO(output_bytes)
        return send_file_response(output, "dados_financeiros.pdf", "application/pdf")

    return "Formato não suportado", 400


# Rota para listar os usuários
@app.route('/admin/usuarios')
def listar_usuarios():
    """
    Lista todos os usuários do sistema para o administrador.

    Restringe o acesso para usuários que não sejam administradores.
    """
    if not session.get('is_admin'):
        flash('Acesso restrito para administradores.', 'danger')
        return redirect(url_for('login'))

    with sqlite3.connect('financeiro.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, username, senha_hash, is_admin, ativo FROM usuarios")
        usuarios = cursor.fetchall()

    return render_template('admin/usuarios.html', usuarios=usuarios)


# Rota para Ativar/Desativar usuário
@app.route('/admin/usuarios/<int:id>/toggle', methods=['POST'])
def toggle_usuario(id):
    """
    Ativa ou desativa um usuário baseado no seu estado atual.
    Apenas administradores podem acessar esta função.
    """
    if not session.get('is_admin'):
        flash('Acesso restrito para administradores.', 'danger')
        return redirect(url_for('login'))

    resultado = executar_consulta(
        "SELECT ativo FROM usuario WHERE id = ?",
        (id,),
        fetchone=True
    )

    if resultado is None:
        flash('Usuário não encontrado.', 'warning')
        return redirect(url_for('listar_usuarios'))

    novo_status = 0 if resultado[0] else 1
    executar_consulta(
        "UPDATE usuarios SET ativo = ? WHERE if = ?",
        (novo_status, id),
        commit=True
    )
    flash('Status do usuário atualizado com sucesso.', 'success')
    return redirect(url_for('listar_usuarios'))


# Rota para Tornar/Remover Admin
@app.route('/admin/toggle_admin/<int:id>', methods=['POST'])
def toggle_admin(id):
    """
    Alterna o status de administrador (is_admin) de um usuário.
    Acesso restrito apenas para administradores.
    """
    if not session.get('is_admin'):
        flash('Acesso restrito para administradores.', 'danger')
        return redirect(url_for('login'))

    resultado = executar_consulta(
        "SELECT is_admin FROM usuarios WHERE id = ?",
        (id,),
        fetchone=True
    )

    if resultado is None:
        flash('Usuário não encontrado.', 'warning')
        return redirect(url_for('listar_usuarios'))

    novo_status = 0 if resultado[0] else 1
    executar_consulta(
        "UPDATE usuarios SET is_admin = ? WHERE id = ?",
        (novo_status, id),
        commit=True
    )
    flash('Permissão de administrador atualizada com sucesso.', 'success')
    return redirect(url_for('listar_usuarios'))


# Rota do termo
@app.route('/termos')
def termos():
    """
    Renderiza a página dos Termos de Uso.
    """
    return render_template("termos.html")


@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    """
    Atualiza os dados do perfil do usuário logado no sistema.

    Valida CPF, data de nascimento e senha (se fornecida).
    Atualiza os dados no banco, incluindo hash da senha se informada.

    Retorna redirect para a página de perfil com mensagem de sucesso ou erro.
    """
    if 'usuario' not in session:
        flash('Você precisa estar logado para editar o perfil.', 'warning')
        return redirect(url_for('login'))

    usuario_id = session['usuario']['id']

    # Coleta dos dados do formulário
    nome = request.form.get('nome')
    sobrenome = request.form.get('sobrenome')
    cpf = request.form.get('cpf')
    nascimento = request.form.get('nascimento')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    celular = request.form.get('celular')
    email = request.form.get('email')
    origem = request.form.get('origem')
    canal = request.form.get('canal')
    username = request.form.get('username')
    senha = request.form.get('senha')

    # Validações
    if not validar_cpf(cpf):
        flash('CPF inválido.', 'danger')
        return redirect(url_for('perfil'))

    if not validar_data(nascimento):
        flash('Data de nascimento inválida.', 'danger')
        return redirect(url_for('perfil'))

    if senha and not senha_segura(senha):
        flash('Senha não atende aos critérios de segurança.', 'danger')
        return redirect(url_for('perfil'))

    # Monta a query com ou sem alteração de senha
    if senha:
        senha_hash = criar_senha_hash(senha)
        query = """
            UPDATE usuarios SET
                nome = ?, sobrenome = ?, cpf = ?, nascimento = ?, cidade = ?, estado = ?,
                celular = ?, email = ?, origem = ?, canal = ?, username = ?, senha = ?
            WHERE id = ?
        """
        params = (nome, sobrenome, cpf, nascimento, cidade, estado,
                  celular, email, origem, canal, username, senha_hash, usuario_id)
    else:
        query = """
            UPDATE usuarios SET
                nome = ?, sobrenome = ?, cpf = ?, nascimento = ?, cidade = ?, estado = ?,
                celular = ?, email = ?, origem = ?, canal = ?, username = ?
            WHERE id = ?
        """
        params = (nome, sobrenome, cpf, nascimento, cidade, estado,
                  celular, email, origem, canal, username, usuario_id)

    try:
        executar_consulta(query, params, commit=True)
        flash('Perfil atualizado com sucesso!', 'success')
        session['usuario']['username'] = username
    except Exception as e:
        print("Erro ao atualizar perfil:", e)
        flash('Erro ao atualizar perfil.', 'danger')

    return redirect(url_for('perfil'))


if __name__ == "__main__":
    app.run(
        ssl_context=('cert.pem', 'private.pem'),
        debug=True
    )
