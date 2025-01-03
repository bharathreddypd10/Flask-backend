"""created foreign key driver_id in servicebookings

Revision ID: a844ea9273b3
Revises: a0ae7a9bd50d
Create Date: 2024-10-29 11:53:24.570567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a844ea9273b3'
down_revision = 'a0ae7a9bd50d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicebookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('driver_id', sa.UUID(), nullable=True))
        batch_op.create_foreign_key(None, 'drivers', ['driver_id'], ['driver_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('servicebookings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('driver_id')

    # ### end Alembic commands ###
