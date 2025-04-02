from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# Conectar ao banco
def conectar_banco():
    return sqlite3.connect("financeiro.db")


# Rota Home
@app.route("/")
def home():
    return render_template("home.html")


# Rota para a página de crédito e salvar dados
@app.route("/credito", methods=["GET", "POST"])
def credito():
    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        categoria = request.form.get("categoria")
        data = request.form.get("data")

        if valor and descricao and tipo and categoria and data:  # Garante que todos os campos estão preenchidos
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO creditos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)",
                           (valor, descricao, tipo, categoria, data))
            conexao.commit()
            conexao.close()

        return redirect(url_for("credito"))

    return render_template("credito.html")


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
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO debitos (valor, descricao, tipo, categoria, data) VALUES (?, ?, ?, ?, ?)",
                           (valor, descricao, tipo, categoria, data))
            conexao.commit()
            conexao.close()

        return redirect(url_for("debito"))

    return render_template("debito.html")


if __name__ == "__main__":
    app.run(debug=True)

