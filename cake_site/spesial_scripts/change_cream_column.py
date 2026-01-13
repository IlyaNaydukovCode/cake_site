from alembic import op
import sqlalchemy as sa

def upgrade():
    # Добавляем новый столбец
    op.add_column('custom_cakes', 
                  sa.Column('creams', sa.JSON(), nullable=True))
    
    # Удаляем старый столбец (если он существует)
    op.drop_column('custom_cakes', 'cream_id')

def downgrade():
    # Откат изменений
    op.add_column('custom_cakes', 
                  sa.Column('cream_id', sa.JSON(), nullable=True))
    op.drop_column('custom_cakes', 'creams')