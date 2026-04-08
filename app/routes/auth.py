from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import ChangePasswordForm, LoginForm, SignupParentForm
from app.funcoes import gerar_hash_senha, verificar_hash_senha
from app.models import User


def get_dashboard_route():
    if current_user.role == "child":
        return "child_dashboard"
    return "parent_dashboard"


@app.route('/', methods=['GET', 'POST'])
def tela_login():
    if current_user.is_authenticated:
        return redirect(url_for(get_dashboard_route()))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()
        if usuario and verificar_hash_senha(usuario.password, form.password.data):
            login_user(usuario)
            if usuario.role == "child":
                return redirect(url_for('child_dashboard'))
            return redirect(url_for('parent_dashboard'))

        flash("Falha no login, e-mail ou senha incorretos", "alert-danger")

    return render_template('login.html', form=form)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash("Logout feito com sucesso", "alert-success")
    return redirect(url_for('tela_login'))


@app.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not verificar_hash_senha(current_user.password, form.current_password.data):
            flash("A senha atual está incorreta.", "alert-danger")
        elif form.new_password.data != form.confirm_password.data:
            flash("A confirmação da nova senha não confere.", "alert-danger")
        elif form.current_password.data == form.new_password.data:
            flash("A nova senha deve ser diferente da senha atual.", "alert-danger")
        else:
            current_user.password = gerar_hash_senha(form.new_password.data)
            db.session.commit()
            flash("Senha atualizada com sucesso.", "alert-success")
            return redirect(url_for(get_dashboard_route()))

    return render_template('change_password.html', form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    if current_user.is_authenticated:
        return redirect(url_for(get_dashboard_route()))

    form_cad = SignupParentForm()
    if form_cad.validate_on_submit():
        usuario = User.query.filter_by(email=form_cad.email.data).first()
        if usuario:
            flash(f"Já existe uma conta criada para o e-mail: {form_cad.email.data}", "alert-danger")
        else:
            senha_hash = gerar_hash_senha(form_cad.password.data)

            usuario = User(
                name=form_cad.name.data,  # type: ignore
                email=form_cad.email.data,  # type: ignore
                password=senha_hash,  # type: ignore
                role='parent'  # type: ignore
            )

            db.session.add(usuario)
            db.session.commit()
            flash(f"Conta criada para o e-mail: {form_cad.email.data}", "alert-success")

            return redirect(url_for('tela_login'))

    return render_template('signup_parent.html', form_cad=form_cad)
