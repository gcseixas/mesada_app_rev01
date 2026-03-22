from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe o e-mail"),
            Email(message="E-mail inválido")
        ]
    )

    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Informe a senha")
        ]
    )

    submit = SubmitField("Entrar")


class SignupParentForm(FlaskForm):
    name = StringField(
        "Nome",
        validators=[
            DataRequired(message="Informe o nome")
        ]
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe o e-mail"),
            Email(message="E-mail inválido")
        ]
    )

    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Informe a senha"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres")
        ]
    )

    submit = SubmitField("Criar conta")
    

class TaskForm(FlaskForm):
    title = StringField(
        "Nome da tarefa",
        validators=[
            DataRequired(message="Informe o nome da tarefa")
        ]
    )

    amount = DecimalField(
        "Valor",
        places=2,
        rounding=None,
        validators=[
            DataRequired(message="Informe o valor da tarefa")
        ]
    )

    submit = SubmitField("Adicionar")
   
   
class SignupChildForm(FlaskForm):
    name = StringField(
        "Nome",
        validators=[
            DataRequired(message="Informe o nome")
        ]
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe o e-mail"),
            Email(message="E-mail inválido")
        ]
    )

    password = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Informe a senha"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres")
        ]
    )

    submit = SubmitField("Criar conta")
    
    