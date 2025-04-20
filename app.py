import os.path
import json
from io import BytesIO
import sqlite3
import bcrypt

import pandas as pd
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from utils import executar_consulta


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
    redirect_url="/login/github/authorized",
)

app.register_blueprint(google_bp, url_prefix="/login")  # Google
app.register_blueprint(github_bp, url_prefix="/login")  # GitHub


# Cria a tabela de usuários
def criar_tabela_usuarios():
    """
    Cria a tabela 'usuarios' no banco de dados, caso ela ainda não exista.
    """
    query = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            ativo INTEGER DEFAULT 1
        )
    '''
    executar_consulta(query, commit=True)


criar_tabela_usuarios()


# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        query = "SELECT id, username, senha_hash, is_admin FROM usuarios WHERE username = ?"
        resultado = executar_consulta(query, (usuario,), fetchone=True)

        if resultado:
            id_usuario, username, senha_hash, is_admin = resultado

            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
                session['usuario'] = {
                    'id': id_usuario,
                    'username': username
                }
                session['is_admin'] = bool(is_admin)

                if session['is_admin']:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))

        flash("Usuário ou senha inválidos", "danger")

    return render_template('login.html')


# Rota de Logon/google
@app.route("/login/google", endpoint="login_google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Erro ao acessar dados do Google", 400

    dados = resp.json()
    email = dados["email"]
    nome = dados.get("name")

    return f"Bem-vindo(a), {nome} ({email})"


# Rota de Logon/Github
@app.route("/login/github", endpoint="login_github")
def login_github():
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
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar o perfil.', 'warning')
        return redirect(url_for('login'))

    usuario_nome = session['usuario']['username']

    query = "SELECT id, username, is_admin, ativo FROM usuarios WHERE username = ?"
    usuario = executar_consulta(query, (usuario_nome,), fetchone=True)

    return render_template('perfil.html', usuario=usuario)


# Rota de Desativação da Conta
@app.route('/desativar_conta/<int:id>', methods=['POST'])
def desativar_conta(id):
    if 'usuario' not in session:
        flash('Você precisa estar logado para fazer isso.', 'danger')
        return redirect(url_for('login'))

    query = "UPDATE usuarios SET ativo = 0 WHERE id = ?"
    executar_consulta(query, (id,), commit=True)

    session.clear()
    flash('Conta desativada com sucesso.', 'success')
    return redirect(url_for('welcome'))


# Roda de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']

        if senha != confirmar_senha:
            flash("As senhas não coincidem", "danger")
            return redirect(url_for('cadastro'))

        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            query = "INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)"
            executar_consulta(query, (usuario, senha_hash), commit=True)
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Usuário já existe", "warning")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')


# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu com sucesso", "success")
    return redirect(url_for('welcome'))


# Rota do Welcome
@app.route('/')
def welcome():
    return render_template("welcome.html")


# Rota Home
@app.route("/home", methods=["GET"])
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    # Filtros
    status_filtro = request.args.get("status")
    data_filtro = request.args.get("data")
    busca = request.args.get("busca", "").lower()

    query = "SELECT * FROM debitos WHERE 1=1"
    params = []

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

    # Pega os dados de crédito
    creditos = executar_consulta("SELECT categoria, SUM(valor) FROM creditos GROUP BY categoria", fetchall=True)
    total_creditos = sum([row[1] for row in creditos])

    # Pega os dados de débitos
    debitos = executar_consulta("SELECT categoria, SUM(valor) FROM debitos GROUP BY categoria", fetchall=True)
    total_debitos = sum([row[1] for row in debitos])

    conexao.close()

    return render_template("home.html",
                           creditos=creditos,
                           debitos=debitos,
                           total_creditos=total_creditos,
                           total_debitos=total_debitos,
                           tabela_debitos=tabela_debitos)


# Rota Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')


# Rota para a página de crédito e salvar dados
@app.route("/credito", methods=["GET", "POST"])
def credito():
    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            query = "INSERT INTO creditos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)"
            parametros = (valor, descricao, tipo, categoria, data)
            executar_consulta(query, parametros, commit=True)

    # Buscar todos os registros da tabela de crédito
    creditos = executar_consulta("SELECT * FROM creditos", fetchall=True)

    return render_template("credito.html", creditos=creditos)


# Rota para página de débito e salvar dados
@app.route("/debito", methods=["GET", "POST"])
def debito():
    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            query = "INSERT INTO debitos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)"
            parametros = (valor, descricao, tipo, categoria, data)
            executar_consulta(query, parametros, commit=True)

    # Buscar todos os registros da tabela de crédito
    debitos = executar_consulta("SELECT * FROM debitos", fetchall=True)

    return render_template("debito.html", debitos=debitos)


# Rota para a página About
@app.route("/about")
def about():
    return render_template("about.html")


# Rota para editar dados da tabela de crédito
@app.route("/editar_credito/<int:id>", methods=["GET", "POST"])
def editar_credito(id):
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
    debito =executar_consulta(query, (id,), fetchone=True)

    return render_template("editar_debito.html", debito=debito)


# Rota para excluir dados da tabela crédito
@app.route("/excluir_credito/<int:id>")
def excluir_credito(id):
    query = "DELETE FROM creditos WHERE id = ?"
    executar_consulta(query, (id,), commit=True)
    return redirect(url_for("credito"))


# Rota para excluir dados da tabela débito
@app.route("/excluir_debito/<int:id>")
def excluir_debito(id):
    query = "DELETE FROM debitos WHERE id = ?"
    executar_consulta(query, (id,), commit=True)
    return redirect(url_for("debito"))


# Rota para atualizar o status do débito
@app.route('/atualizar-status-debito/<int:id>', methods=['POST'])
def atualizar_status_debito(id):
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
    with sqlite3.connect('financeiro.db') as conexao:
        df_creditos = pd.read_sql_query("SELECT * FROM creditos", conexao)
        df_debitos = pd.read_sql_query("SELECT * FROM debitos", conexao)

    if formato == 'xls':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_creditos.to_excel(writer, sheet_name='Créditos', index=False)
            df_debitos.to_excel(writer, sheet_name='Débitos', index=False)
        output.seek(0)
        return send_file(output, download_name='dados_financeiros.xlsx', as_attachment=True)

    elif formato == 'json':
        dados = {
            "creditos": df_creditos.to_dict(orient="records"),
            "debitos": df_debitos.to_dict(orient="records")
        }
        output = BytesIO()
        output.write(json.dumps(dados, indent=4).encode('utf-8'))
        output.seek(0)
        return send_file(output, download_name='dados_financeiro.json', as_attachment=True)

    elif formato == 'pdf':
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "Relatório de Créditos", ln=True, align="C")
        for _, row in df_creditos.iterrows():
            pdf.cell(0, 10, txt=str(row.to_dict()), ln=True)

        pdf.add_page()
        pdf.cell(200, 10, "Relatório de Débitos", ln=True, align="C")
        for _, row in df_debitos.iterrows():
            pdf.cell(0, 10, txt=str(row.to_dict()), ln=True)

        output_bytes = pdf.output(dest='S').encode('latin-1')
        output = BytesIO(output_bytes)
        return send_file(output, download_name="dados_financeiro.pdf", as_attachment=True)

    return "Formato não suportado", 400


# Rota para listar os usuários
@app.route('/admin/usuários')
def listar_usuarios():
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
    resultado = executar_consulta(
        "SELECT ativo FROM usuarios WHERE id = ?",
        (id,),
        fetchone=True
    )

    if resultado is not None:
        novo_status = 0 if resultado[0] else 1
        executar_consulta(
            "UPDATE usuarios SET ativo = ? WHERE id = ?",
            (novo_status, id),
            commit=True
        )

    return redirect(url_for('listar_usuarios'))


# Rota para Tornar/Remover Admin
@app.route('/admin/toggle_admin/<int:id>', methods=['POST'])
def toggle_admin(id):
    if not session.get('is_admin'):
        flash('Acesso restrito para administrator.', 'danger')
        return redirect(url_for('login'))

    resultado = executar_consulta(
        "SELECT is_admin FROM usuarios WHERE id = ?",
        (id,),
        fetchone=True
    )

    if resultado:
        novo_status = 0 if resultado[0] else 1
        executar_consulta(
            "UPDATE usuarios SET is_admin = ? WHERE id = ?",
            (novo_status, id),
            commit=True
        )

    return redirect(url_for('listar_usuarios'))


if __name__ == "__main__":
    app.run(debug=True)
