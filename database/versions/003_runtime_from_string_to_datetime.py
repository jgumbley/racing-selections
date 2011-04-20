from sqlalchemy import *
from migrate import *

meta=MetaData()

run_table_new = Table(
        'runs', meta,
        Column('id', Integer, primary_key=True),
        Column('location', String, nullable=False),
        Column('nag', String, nullable=False),
        Column('start_time', DateTime, nullable=True),
        Column('created_date', DateTime(timezone=False)),
        )

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    run_table_new.c.start_time.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    run_table_new.c.start_time.drop()
