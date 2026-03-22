from flask import render_template, redirect, url_for
from app import app
from app.models import TaskSubmission, Task
from flask_login import login_required, current_user


@app.route('/child_dashboard')
@login_required
def child_dashboard():
    pending_tasks = TaskSubmission.query.filter_by(
        id = current_user.id,
        status = "pending"
    ).all()
    
    if current_user.role != "child":
        return redirect(url_for("parent_dashboard"))
    
    return render_template(
        'child_dashboard.html',
        child=current_user,
        pending_tasks = pending_tasks
    )


@app.route('/lancar_tareda', methods=['GET', 'POST'])
@login_required
def lancar_tareda():
    
    tasks = Task.query.filter_by(
        parent_id=current_user.parent_id,
        active=True
    ).all()
    
    return render_template(
        'submit_task.html', 
        tasks=tasks   
    )
 