"""Create servicebookings table

Revision ID: 5a395e3289b4
Revises: bf6a7355e1d4
Create Date: 2024-10-22 17:33:36.504994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a395e3289b4'
down_revision = 'bf6a7355e1d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('servicebookings',
    sa.Column('booking_id', sa.UUID(), nullable=False),
    sa.Column('vehicle_type', sa.String(length=50), nullable=False),
    sa.Column('vehicle_number', sa.String(length=20), nullable=False),
    sa.Column('service_type', sa.String(length=100), nullable=False),
    sa.Column('preferred_date', sa.Date(), nullable=False),
    sa.Column('preferred_time', sa.Time(), nullable=False),
    sa.Column('pickup_location', sa.String(length=200), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('booking_id'),
    sa.UniqueConstraint('vehicle_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('servicebookings')
    # ### end Alembic commands ###
