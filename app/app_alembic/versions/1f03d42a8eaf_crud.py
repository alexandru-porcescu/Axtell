"""CRUD

Revision ID: 1f03d42a8eaf
Revises: 
Create Date: 2018-07-11 00:29:08.597685+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f03d42a8eaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('category_id', 'post_id')
    )
    op.add_column('answer_comments', sa.Column('deleted', sa.Boolean(), nullable=False))
    op.alter_column('answer_comments', 'text',
               existing_type=mysql.VARCHAR(length=240),
               nullable=False)
    op.add_column('answers', sa.Column('deleted', sa.Boolean(), nullable=False))
    op.add_column('post_comments', sa.Column('deleted', sa.Boolean(), nullable=False))
    op.alter_column('post_comments', 'text',
               existing_type=mysql.VARCHAR(length=240),
               nullable=False)
    op.add_column('posts', sa.Column('deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'deleted')
    op.alter_column('post_comments', 'text',
               existing_type=mysql.VARCHAR(length=240),
               nullable=True)
    op.drop_column('post_comments', 'deleted')
    op.drop_column('answers', 'deleted')
    op.alter_column('answer_comments', 'text',
               existing_type=mysql.VARCHAR(length=240),
               nullable=True)
    op.drop_column('answer_comments', 'deleted')
    op.drop_table('post_categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
