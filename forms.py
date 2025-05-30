from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TelField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[
        DataRequired(),
        Regexp(r'ˆ\d{11}$', message="CPF deve ter 11 dígitos.")
    ])
    nascimento = DateField('Data de Nascimento', format='%d-%m-%Y', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    celular = TelField('Celular', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    origem = StringField('Como conheceu')
    canal = StringField('Canal preferido')
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres.")
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('senha', message="As senhas devem coincidir.")
    ])
    termos = BooleanField('Aceito os termos de uso', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')