"""Update user model to int id

Revision ID: 1b3536d9dcd4
Revises: 1234567890ab
Create Date: 2026-02-04 02:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '1b3536d9dcd4'
down_revision: Union[str, None] = '1234567890ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the foreign key constraint first
    op.drop_constraint('task_user_id_fkey', 'task', type_='foreignkey')

    # Drop the old user table (with UUID id)
    op.drop_table('user')

    # Create the new users table (with integer id)
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.Index('ix_users_email', 'email')
    )

    # Update the task table to reference the new users table
    # Since we're changing from user.id (UUID) to users.id (Integer), we need to update the foreign key
    # First drop the task table and recreate it with the proper reference
    op.drop_table('task')

    # Recreate task table with proper reference to users table
    op.create_table('task',
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),  # Changed to Integer
        sa.Column('id', sa.Integer(), nullable=False),       # Changed to Integer
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),  # Changed to reference 'users'
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # Recreate the old user table structure
    op.drop_table('users')

    op.create_table('user',
        sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )