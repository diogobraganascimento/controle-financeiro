import os.path
import json
from io import BytesIO
import sqlite3

import pandas as pd
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, send_file


app = Flask(__name__)


# Rota Home
@app.route("/", methods=["GET"])
def home():
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

    cursor.execute(query, params)
    tabela_debitos = cursor.fetchall()

    # Aplica filtro de busca por descrição (índice 2 = descrição)
    if busca:
        tabela_debitos = [debito for debito in tabela_debitos if busca in debito[2].lower()]

    # Pega os dados de crédito
    cursor.execute("SELECT categoria, SUM(valor) FROM creditos GROUP BY categoria")
    creditos = cursor.fetchall()
    total_creditos = sum([row[1] for row in creditos])

    # Pega os dados de débitos
    cursor.execute("SELECT categoria, SUM(valor) FROM debitos GROUP BY categoria")
    debitos = cursor.fetchall()
    total_debitos = sum([row[1] for row in debitos])

    conexao.close()

    return render_template("home.html",
                           creditos=creditos,
                           debitos=debitos,
                           total_creditos=total_creditos,
                           total_debitos=total_debitos,
                           tabela_debitos=tabela_debitos)


# Rota para a página de crédito e salvar dados
@app.route("/credito", methods=["GET", "POST"])
def credito():
    conaxao = sqlite3.connect("financeiro.db")
    cursor = conaxao.cursor()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            cursor.execute("INSERT INTO creditos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)",
                           (valor, descricao, tipo, categoria, data))
            conaxao.commit()

    # Buscar todos os registros da tabela de crédito
    cursor.execute("SELECT * FROM creditos")
    creditos = cursor.fetchall()

    conaxao.close()
    return render_template("credito.html", creditos=creditos)


# Rota para página de débito e salvar dados
@app.route("/debito", methods=["GET", "POST"])
def debito():
    conaxao = sqlite3.connect("financeiro.db")
    cursor = conaxao.cursor()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:
            cursor.execute("INSERT INTO debitos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)",
                           (valor, descricao, tipo, categoria, data))
            conaxao.commit()

    # Buscar todos os registros da tabela de crédito
    cursor.execute("SELECT * FROM debitos")
    debitos = cursor.fetchall()

    conaxao.close()
    return render_template("debito.html", debitos=debitos)


# Rota para editar dados da tabela de crédito
@app.route("/editar_credito/<int:id>", methods=["GET", "POST"])
def editar_credito(id):
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        cursor.execute("UPDATE creditos SET valor=?, descricao=?, tipo=?, categoria=?, data=? WHERE id=?",
                       (valor, descricao, tipo, categoria, data, id))
        conexao.commit()
        conexao.close()
        return redirect(url_for("credito"))

    cursor.execute("SELECT * FROM creditos WHERE id=?", (id,))
    credito = cursor.fetchone()
    conexao.close()

    return render_template("editar_credito.html", credito=credito)


# Rota para editar dados da tabela de débito
@app.route("/editar_debito/<int:id>", methods=["GET", "POST"])
def editar_debito(id):
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        cursor.execute("UPDATE debitos SET valor=?, descricao=?, tipo=?, categoria=?, data=? WHERE id=?",
                       (valor, descricao, tipo, categoria, data, id))
        conexao.commit()
        conexao.close()
        return redirect(url_for("debito"))

    cursor.execute("SELECT * FROM debitos WHERE id=?", (id,))
    debito = cursor.fetchone()
    conexao.close()

    return render_template("editar_debito.html", debito=debito)


# Rota para excluir dados da tabela crédito
@app.route("/excluir_credito/<int:id>")
def excluir_credito(id):
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM creditos WHERE id=?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("credito"))


# Rota para excluir dados da tabela débito
@app.route("/excluir_debito/<int:id>")
def excluir_debito(id):
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM debitos WHERE id=?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("debito"))


# Rota para atualizar o status do débito
@app.route('/atualizar-status-debito/<int:id>', methods=['POST'])
def atualizar_status_debito(id):
    status = request.form.get('status')
    data_agendada = request.form.get('data_agendada', None)

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    if status == 'Agendado' and data_agendada:
        cursor.execute("UPDATE debitos SET status = ?, data_agendada = ? WHERE id = ?", (status, data_agendada, id))
    else:
        cursor.execute("UPDATE debitos SET status = ?, data_agendada = NULL WHERE id = ?", (status, id))

    conexao.commit()
    conexao.close()
    return redirect(url_for('debito'))


@app.route('/exportar/<formato>')
def exportar_dados(formato):
    conexao = sqlite3.connect('financeiro.db')
    df_creditos = pd.read_sql_query("SELECT * FROM creditos", conexao)
    df_debitos = pd.read_sql_query("SELECT * FROM debitos", conexao)
    conexao.close()

    # Baixar em XLS
    if formato == 'xls':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_creditos.to_excel(writer, sheet_name='Créditos', index=False)
            df_debitos.to_excel(writer, sheet_name='Débitos', index=False)
        output.seek(0)
        return send_file(output, download_name='dados_financeiros.xlsx', as_attachment=True)

    # Baixar em JSON
    elif formato == 'json':
        dados = {
            "creditos": df_creditos.to_dict(orient="records"),
            "debitos": df_debitos.to_dict(orient="records")
        }
        output = BytesIO()
        output.write(json.dumps(dados, indent=4).encode('utf-8'))
        output.seek(0)
        return send_file(output, download_name='dados_financeiro.json', as_attachment=True)

    # Baixar em PDF
    elif formato == 'pdf':
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, "Relatório de Créditos", ln=True, align="C")
        for index, row in df_creditos.iterrows():
            pdf.cell(0, 10, txt=str(row.to_dict()), ln=True)

        pdf.add_page()
        pdf.cell(200, 10, "Relatório de Débitos", ln=True, align="C")
        for index, row in df_debitos.iterrows():
            pdf.cell(0, 10, txt=str(row.to_dict()), ln=True)

        output_bytes = pdf.output(dest='S').encode('latin-1')
        output = BytesIO(output_bytes)

        return send_file(output, download_name="dados_financeiro.pdf", as_attachment=True)

    return "Formato não suportado", 400


if __name__ == "__main__":
    app.run(debug=True)
