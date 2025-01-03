"""Initial migration

Revision ID: b0268da0ee3d
Revises: 
Create Date: 2024-09-02 15:08:39.330174

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b0268da0ee3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.drop_table('students')
    op.drop_table('employee')
    op.drop_table('funds')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('funds',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='funds_pkey')
    )
    op.create_table('employee',
    sa.Column('emp_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('emp_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('pwd', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('salary', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('emp_id', name='employee_pkey'),
    sa.UniqueConstraint('email', name='employee_email_key')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='students_pkey')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
