from sqlalchemy import *
from migrate import *

meta=MetaData()

nags_table = Table(
        'nags', meta,
        Column('name', String(length=None),  primary_key=True, nullable=False),
        Column('created_date', DateTime(timezone=False)),
        )

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    nags_table.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    nags_table.drop()
