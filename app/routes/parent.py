from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.models import User, Task
from app.forms import TaskForm, SignupChildForm
from flask_login import login_required, current_user


@app.route('/parent_dashboard', methods=['GET', 'POST'])
@login_required
def parent_dashboard():

    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    children = current_user.get_children()

    return render_template(
        'parent_dashboard.html',
        children=children
    )

 
@app.route('/configurar_tarefa', methods=['GET', 'POST'])
@login_required
def configurar_tarefa():
    
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title = form.title.data, # type: ignore
            amount = form.amount.data, # type: ignore
            parent_id = 1, # type: ignore
            
        )
        
        db.session.add(task)
        db.session.add(task)
        db.session.commit()
        
        flash(f"Tarefa '{form.title.data}' criada com sucesso")
        return redirect(url_for('configurar_tarefa'))
      
    else:
        
        tasks = Task.query.all()
            
        return render_template('configure_tasks.html', tasks=tasks, form=form)
    
    
@app.route('/remover_tarefa', methods=['POST'])
@login_required
def remover_tarefa():
    task_id = request.form.get('task_id')

    if not task_id:
        return redirect(url_for('configurar_tarefa'))

    task = Task.query.get(int(task_id))

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('configurar_tarefa'))

@app.route('/cadastrar_filho', methods=['GET', 'POST'])
def tela_cadastro_filho():
    
    form_cad = SignupChildForm()
    if form_cad.validate_on_submit():
        usuario = User.query.filter_by(email=form_cad.email.data).first()
        if usuario:
            flash(f"Já existe uma conta criada para o e-mail: {form_cad.email.data}")
        
        else:
            
            senha_hash = bcrypt.generate_password_hash(form_cad.password.data)
            
            usuario = User(
                name = form_cad.name.data, # type: ignore
                email = form_cad.email.data, # type: ignore
                password = senha_hash, # type: ignore
                role = 'child',   # type: ignore
                parent_id = current_user.id # type: ignore
            )
            
            db.session.add(usuario)
            db.session.commit()
            flash(f"Conta criada para o e-mail: {form_cad.email.data}")
            
            return redirect(url_for('parent_dashboard'))
    
    return render_template('cadastrar_filho.html', form_cad=form_cad) 