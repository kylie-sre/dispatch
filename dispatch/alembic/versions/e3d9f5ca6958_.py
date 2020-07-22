"""Adding reported_at timestamp

Revision ID: e3d9f5ca6958
Revises: d0501fc6be89
Create Date: 2020-02-04 10:40:49.342897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e3d9f5ca6958"
down_revision = "d0501fc6be89"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("incident", sa.Column("reported_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("incident", "reported_at")
    # ### end Alembic commands ###
