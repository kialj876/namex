"""empty message

Revision ID: 42681ac46798
Revises: c0f893cd0dee
Create Date: 2018-06-05 14:44:37.438142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '42681ac46798'
down_revision = 'c0f893cd0dee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    state_table = op.create_table('states',
    sa.Column('cd', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('cd')
    )
    op.add_column('events', sa.Column('state_cd', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'events', 'states', ['state_cd'], ['cd'])
    op.add_column('requests', sa.Column('stateCd', sa.String(length=40), nullable=True))
    op.create_foreign_key(None, 'requests', 'states', ['stateCd'], ['cd'])
    op.drop_column('requests', 'state')
    # ### end Alembic commands ###

    op.bulk_insert(
        state_table,
        [
            {'cd': 'DRAFT', 'description': 'Unexamined name, submitted by a client'},
            {'cd': 'INPROGRESS', 'description': 'An examiner is working on this request'},
            {'cd': 'CANCELLED', 'description': 'The request is cancelled and cannot be changed'},
            {'cd': 'HOLD', 'description': 'A name approval was halted for some reason'},
            {'cd': 'APPROVED', 'description': 'Approved request, this is a final state'},
            {'cd': 'REJECTED', 'description': 'Rejected request, this is a final state'},
            {'cd': 'CONDITIONAL', 'description': 'Approved, but with conditions to be met. This is a final state'}
        ]
    )

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('state', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.drop_column('requests', 'stateCd')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'state_cd')
    op.drop_table('states')
    # ### end Alembic commands ###
