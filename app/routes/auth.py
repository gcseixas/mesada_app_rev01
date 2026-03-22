from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, SignupParentForm
from app.models import User
from flask_login import login_user, logout_user, login_required

@app.route('/', methods=['GET', 'POST'])
def tela_login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()
        if usuario and form.password.data == usuario.password:
            login_user(usuario)
            return redirect(url_for('parent_dashboard'))
        else:
            flash(f"Falha no login, e-mail ou senha incorretos", "alert-danger")
                
    return render_template('login.html', form=form)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f"Logaut feito com sucesso", "alert-success")
    return redirect(url_for('tela_login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def tela_cadastro():
    
    form_cad = SignupParentForm()
    if form_cad.validate_on_submit():
        usuario = User.query.filter_by(email=form_cad.email.data).first()
        if usuario:
            flash(f"Já existe uma conta criada para o e-mail: {form_cad.email.data}")
        
        else:
            
            usuario = User(
                name = form_cad.name.data, # type: ignore
                email = form_cad.email.data, # type: ignore
                password = form_cad.password.data, # type: ignore
                role = 'parent'   # type: ignore
            )
            
            db.session.add(usuario)
            db.session.commit()
            flash(f"Conta criada para o e-mail: {form_cad.email.data}")
            
            return redirect(url_for('tela_login'))
    
    return render_template('signup_parent.html', form_cad=form_cad)