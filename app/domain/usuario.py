"""
Entidade de domínio para o usuário do sistema.
"""

from werkzeug.security import check_password_hash, generate_password_hash


class Usuario:
    """
    Representa o usuário do sistema.
    
    A senha nunca é armazenada em texto puro: apensa o hash gerado por generate_password_hash() é guardado.
    Usuario.criar() é a forma recomendada de criar um novo usuário a partir de uma senha em texto puro;
    o construtor normal espera um hash já calculado (usado pelo mapper, ao reconstruir a partir do banco).
    """

    def __init__(
        self,
        username: str,
        senha_hash: str,
        id: int | None = None,
    ):
        self.id = id
        self.username = username
        self.senha_hash = senha_hash

    @property
    def username(self) -> str:
        """Retorna o nome de usuário."""

        return self._username

    @username.setter
    def username(self, username: str):
        """Define o nome de usuário."""

        if not isinstance(username, str):
            raise TypeError("O username deve ser uma string.")

        if not username.strip():
            raise ValueError("O username é obrigatório.")

        self._username = username.strip()

    @property
    def senha_hash(self) -> str:
        """Retorna o hash da senha."""

        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, senha_hash: str):
        """Define o hash da senha."""

        if not isinstance(senha_hash, str) or not senha_hash:
            raise ValueError("O hash da senha é obrigatório.")

        self._senha_hash = senha_hash

    @classmethod
    def criar(cls, username: str, senha: str) -> "Usuario":
        """
        Cria um novo usuário a partir de uma senha em texto puro, calculando o hash antes de armazená-la. Este é o único
        ponto do sistema por onde uma senha em texto puro deve passar.
        """

        if not isinstance(senha, str) or len(senha) < 8:
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres."
            )

        return cls(
            username=username,
            senha_hash=generate_password_hash(senha),
        )

    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se a senha em texto puro corresponde ao hash armazenado.
        """

        return check_password_hash(self.senha_hash, senha)
