from alembic import context
from sqlalchemy import engine_from_config, pool
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
from users.models import User
from cakes.models import Cake, CakeLayer, Cream, Filling, Decoration
from constructor.models import CustomCake
from orders.models import Order, Payment

connectable = engine

def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()