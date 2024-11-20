"""Create services table

Revision ID: 43959c890348
Revises: 5a395e3289b4
Create Date: 2024-10-23 16:10:31.294277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43959c890348'
down_revision = '5a395e3289b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('service_id', sa.UUID(), nullable=False),
    sa.Column('service_type', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('service_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    # ### end Alembic commands ###
