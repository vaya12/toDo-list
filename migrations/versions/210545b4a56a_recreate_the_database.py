"""Recreate the database

Revision ID: 210545b4a56a
Revises: c2e86035e9a9
Create Date: 2024-01-20 23:34:43.729467

"""
from alembic import op
import sqlalchemy as sa

revision = '210545b4a56a'
down_revision = 'c2e86035e9a9'
branch_labels = None
depends_on = None

def upgrade():
    op.rename_table('task', 'task_old')

    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute('INSERT INTO task (id, description) SELECT id, description FROM task_old')

    op.drop_table('task_old')

def downgrade():
    raise NotImplementedError("Downgrade not supported for this migration")
