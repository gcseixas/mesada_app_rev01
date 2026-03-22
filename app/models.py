from app import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return User.query.get(int(id_usuario))


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # "parent" ou "child"
    role = db.Column(db.String(20), nullable=False)

    # Auto-relacionamento (pai -> filhos)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    parent = db.relationship(
        "User",
        remote_side=[id],
        backref="children"
    )
    
    def get_children(self):
        if self.role != "parent":
            return []

        return self.children # type: ignore


    def __repr__(self):
        return f"<User {self.id} {self.name} ({self.role})>"



class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Quem criou a tarefa (pai)
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    active = db.Column(db.Boolean, default=True)

    parent = db.relationship(
        "User",
        backref="tasks"
    )

    def __repr__(self):
        return f"<Task {self.id} {self.title} R${self.amount}>"


class TaskSubmission(db.Model):
    __tablename__ = "task_submissions"

    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    note = db.Column(db.String(255))

    # pending | approved | rejected
    status = db.Column(db.String(20), nullable=False, default="pending")

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    task = db.relationship("Task")
    child = db.relationship("User")

    def __repr__(self):
        return f"<TaskSubmission {self.id} {self.status}>"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    description = db.Column(db.String(255), nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    child = db.relationship("User", backref="transactions")

    def __repr__(self):
        return f"<Transaction {self.id} R${self.amount}>"
