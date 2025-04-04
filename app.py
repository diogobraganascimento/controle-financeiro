import os.path

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Rota Home
@app.route("/")
def home():
    return render_template("home.html")


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


# Rota para excluir dados da tabela crédito
@app.route("/excluir_credito/<int:id>")
def excluir_credito(id):
    conexao = sqlite3.connect("financeiro.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM creditos WHERE id=?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("credito"))


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
            conexao = sqlite3.connect("financeiro.db")
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO debitos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)",
                           (valor, descricao, tipo, categoria, data))
            conexao.commit()
            conexao.close()

        return redirect(url_for("debito"))

    return render_template("debito.html")


if __name__ == "__main__":
    app.run(debug=True)
