from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import TaskSubmission, Task
from flask_login import login_required, current_user


@app.route('/child_dashboard')
@login_required
def child_dashboard():
    if current_user.role != "child":
        return redirect(url_for("parent_dashboard"))

    pending_tasks = TaskSubmission.query.filter_by(
        child_id=current_user.id,
        status="pending"
    ).all()

    return render_template(
        'child_dashboard.html',
        child=current_user,
        pending_tasks=pending_tasks
    )


@app.route('/lancar_tareda', methods=['GET', 'POST'])
@login_required
def lancar_tareda():
    if current_user.role != "child":
        return redirect(url_for("parent_dashboard"))

    tasks = Task.query.filter_by(
        parent_id=current_user.parent_id,
        active=True
    ).all()

    if request.method == "POST":
        task_id = request.form.get("task_id", type=int)
        note = request.form.get("note", "").strip()

        if len(note) > 120:
            flash("A observação da tarefa deve ter no máximo 120 caracteres.", "alert-danger")
            return redirect(url_for("lancar_tareda"))

        task = Task.query.filter_by(
            id=task_id,
            parent_id=current_user.parent_id,
            active=True
        ).first()

        if not task:
            flash("Selecione uma tarefa válida.", "alert-danger")
            return redirect(url_for("lancar_tareda"))

        submission = TaskSubmission(
            task_id=task.id,
            child_id=current_user.id,
            note=note or None,
            status="pending",
        )

        db.session.add(submission)
        db.session.commit()
        flash("Tarefa enviada para aprovação com sucesso.", "alert-success")
        return redirect(url_for("child_dashboard"))

    return render_template(
        'submit_task.html',
        tasks=tasks
    )
