from sqlalchemy import *
from migrate import *

meta=MetaData()

run_table = Table(
        'runs', meta,
        Column('id', Integer, primary_key=True),
        Column('location', String, nullable=False),
        Column('nag', String, nullable=False),
        Column('time', String, nullable=False),
        Column('created_date', DateTime(timezone=False)),
        )

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    run_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    run_table.drop()
