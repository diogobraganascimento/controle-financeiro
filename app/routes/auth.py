"""
Rotas de autenticação (login e logout).
"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.security import UsuarioSession
from app.services.auth_service import CredenciaisInvalidasError, autenticar

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Exibe o formulário de login (GET) e processa a autenticação (POST).
    """

    if request.method == "POST":
        username = request.form.get("username", "")
        senha = request.form.get("senha", "")

        try:
            usuario = autenticar(username=username, senha=senha)
        except CredenciaisInvalidasError as erro:
            return render_template(
                "auth/login.html",
                erro=str(erro),
                username=username,
            )

        login_user(UsuarioSession(usuario))

        return redirect(url_for("home.home"))

    return render_template("auth/login.html", erro=None, username="")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Encerra a sessão do usuário logado.
    """

    logout_user()

    return redirect(url_for("auth.login"))
