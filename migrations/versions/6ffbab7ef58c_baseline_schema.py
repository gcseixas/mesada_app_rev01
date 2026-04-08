"""baseline schema

Revision ID: 6ffbab7ef58c
Revises: 
Create Date: 2026-04-08 12:27:58.462835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '6ffbab7ef58c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    table_names = set(inspector.get_table_names())

    if 'users' not in table_names:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('password', sa.String(length=255), nullable=False),
            sa.Column('role', sa.String(length=20), nullable=False),
            sa.Column('parent_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['parent_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )
        table_names.add('users')

    if 'tasks' not in table_names:
        op.create_table(
            'tasks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('parent_id', sa.Integer(), nullable=False),
            sa.Column('active', sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(['parent_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id')
        )
        table_names.add('tasks')

    if 'task_submissions' not in table_names:
        op.create_table(
            'task_submissions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('task_id', sa.Integer(), nullable=False),
            sa.Column('child_id', sa.Integer(), nullable=False),
            sa.Column('note', sa.String(length=255), nullable=True),
            sa.Column('rejection_reason', sa.String(length=255), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('submitted_at', sa.DateTime(), nullable=True),
            sa.Column('approved_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['child_id'], ['users.id']),
            sa.ForeignKeyConstraint(['task_id'], ['tasks.id']),
            sa.PrimaryKeyConstraint('id')
        )
        table_names.add('task_submissions')
    else:
        task_submission_columns = {
            column['name']
            for column in inspector.get_columns('task_submissions')
        }
        if 'rejection_reason' not in task_submission_columns:
            op.add_column(
                'task_submissions',
                sa.Column('rejection_reason', sa.String(length=255), nullable=True)
            )

    if 'transactions' not in table_names:
        op.create_table(
            'transactions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('child_id', sa.Integer(), nullable=False),
            sa.Column('description', sa.String(length=255), nullable=False),
            sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['child_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    table_names = set(inspector.get_table_names())

    if 'transactions' in table_names:
        op.drop_table('transactions')
    if 'task_submissions' in table_names:
        op.drop_table('task_submissions')
    if 'tasks' in table_names:
        op.drop_table('tasks')
    if 'users' in table_names:
        op.drop_table('users')
