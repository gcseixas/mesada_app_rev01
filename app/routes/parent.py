from decimal import Decimal, InvalidOperation

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import app, db
from app.funcoes import gerar_hash_senha, agora_brasil
from app.models import User, Task, TaskSubmission, Transaction
from app.forms import TaskForm, SignupChildForm


@app.route('/parent_dashboard', methods=['GET', 'POST'])
@login_required
def parent_dashboard():

    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    children = current_user.get_children()
    total = sum((child.balance for child in children), Decimal("0.00"))
    total_approved = sum((child.approved_total for child in children), Decimal("0.00"))
    total_paid = sum((child.paid_total for child in children), Decimal("0.00"))

    return render_template(
        'parent_dashboard.html',
        children=children,
        total=total,
        total_approved=total_approved,
        total_paid=total_paid
    )


@app.route('/filho/<int:child_id>')
@login_required
def ver_filho(child_id):
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    child = User.query.filter_by(
        id=child_id,
        role='child',
        parent_id=current_user.id
    ).first_or_404()

    submissions = TaskSubmission.query.filter_by(
        child_id=child.id
    ).order_by(TaskSubmission.submitted_at.desc()).all()

    transactions = Transaction.query.filter_by(
        child_id=child.id
    ).order_by(Transaction.created_at.desc()).all()

    return render_template(
        'child_detail.html',
        child=child,
        submissions=submissions,
        balance=child.balance,
        transactions=transactions
    )


@app.route('/filho/<int:child_id>/pagamentos', methods=['POST'])
@login_required
def registrar_pagamento(child_id):
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    child = User.query.filter_by(
        id=child_id,
        role='child',
        parent_id=current_user.id
    ).first_or_404()

    if child.balance <= 0:
        flash("Esse filho não possui saldo pendente para pagamento.", "alert-warning")
        return redirect(url_for('ver_filho', child_id=child.id))

    raw_amount = (request.form.get('amount') or '').replace(',', '.').strip()
    description = (request.form.get('description') or '').strip() or "Pagamento realizado pelo responsável"

    if len(description) > 120:
        flash("A descrição do pagamento deve ter no máximo 120 caracteres.", "alert-danger")
        return redirect(url_for('ver_filho', child_id=child.id))

    try:
        amount = Decimal(raw_amount).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        flash("Informe um valor de pagamento válido.", "alert-danger")
        return redirect(url_for('ver_filho', child_id=child.id))

    if amount <= 0:
        flash("O pagamento deve ser maior que zero.", "alert-danger")
        return redirect(url_for('ver_filho', child_id=child.id))

    if amount > child.balance:
        flash("O pagamento não pode ser maior que o saldo pendente.", "alert-danger")
        return redirect(url_for('ver_filho', child_id=child.id))

    transaction = Transaction(
        child_id=child.id,
        description=description,
        amount=-amount
    )

    db.session.add(transaction)
    db.session.commit()
    flash("Pagamento registrado com sucesso.", "alert-success")
    return redirect(url_for('ver_filho', child_id=child.id))


@app.route('/filho/<int:child_id>/aprovacoes')
@login_required
def aprovacoes_filho(child_id):
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    child = User.query.filter_by(
        id=child_id,
        role='child',
        parent_id=current_user.id
    ).first_or_404()

    pending = TaskSubmission.query.filter_by(
        child_id=child.id,
        status='pending'
    ).order_by(TaskSubmission.submitted_at.asc()).all()

    return render_template(
        'aprove_tasks.html',
        child=child,
        pending=pending
    )


@app.route('/aprovacoes/<int:submission_id>/<action>', methods=['POST'])
@login_required
def atualizar_aprovacao(submission_id, action):
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    submission = TaskSubmission.query.get_or_404(submission_id)

    if submission.child.parent_id != current_user.id:
        flash("Você não pode alterar esse lançamento.", "alert-danger")
        return redirect(url_for('parent_dashboard'))

    if submission.status != 'pending':
        flash("Esse lançamento já foi processado.", "alert-warning")
        return redirect(url_for('aprovacoes_filho', child_id=submission.child_id))

    if action == 'approve':
        submission.status = 'approved'
        submission.approved_at = agora_brasil()
        submission.rejection_reason = None
        transaction = Transaction(
            child_id=submission.child_id,
            description=submission.task.title,
            amount=submission.task.amount
        )
        db.session.add(transaction)
        flash("Tarefa aprovada com sucesso.", "alert-success")
    elif action == 'reject':
        rejection_reason = request.form.get('rejection_reason', '').strip()
        if not rejection_reason:
            flash("Informe o motivo da reprovação.", "alert-danger")
            return redirect(url_for('aprovacoes_filho', child_id=submission.child_id))

        submission.status = 'rejected'
        submission.rejection_reason = rejection_reason
        flash("Tarefa rejeitada.", "alert-warning")
    else:
        flash("Ação inválida.", "alert-danger")
        return redirect(url_for('aprovacoes_filho', child_id=submission.child_id))

    db.session.commit()
    return redirect(url_for('aprovacoes_filho', child_id=submission.child_id))


@app.route('/configurar_tarefa', methods=['GET', 'POST'])
@login_required
def configurar_tarefa():
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,  # type: ignore
            amount=form.amount.data,  # type: ignore
            parent_id=current_user.id,  # type: ignore
        )

        db.session.add(task)
        db.session.commit()

        flash(f"Tarefa '{form.title.data}' criada com sucesso")
        return redirect(url_for('configurar_tarefa'))

    tasks = Task.query.filter_by(parent_id=current_user.id).all()

    return render_template('configure_tasks.html', tasks=tasks, form=form)


@app.route('/remover_tarefa', methods=['POST'])
@login_required
def remover_tarefa():
    task_id = request.form.get('task_id')

    if not task_id:
        return redirect(url_for('configurar_tarefa'))

    task = Task.query.filter_by(
        id=int(task_id),
        parent_id=current_user.id
    ).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('configurar_tarefa'))


@app.route('/cadastrar_filho', methods=['GET', 'POST'])
@login_required
def tela_cadastro_filho():
    if current_user.role != "parent":
        return redirect(url_for("child_dashboard"))

    form_cad = SignupChildForm()
    if form_cad.validate_on_submit():
        usuario = User.query.filter_by(email=form_cad.email.data).first()
        if usuario:
            flash(f"Já existe uma conta criada para o e-mail: {form_cad.email.data}")
        else:
            senha_hash = gerar_hash_senha(form_cad.password.data)

            usuario = User(
                name=form_cad.name.data,  # type: ignore
                email=form_cad.email.data,  # type: ignore
                password=senha_hash,  # type: ignore
                role='child',  # type: ignore
                parent_id=current_user.id  # type: ignore
            )

            db.session.add(usuario)
            db.session.commit()
            flash(f"Conta criada para o e-mail: {form_cad.email.data}")

            return redirect(url_for('parent_dashboard'))

    return render_template('cadastrar_filho.html', form_cad=form_cad)
