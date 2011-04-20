from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, MetaData
from sqlalchemy.orm import sessionmaker, mapper 
from datetime import datetime

meta = MetaData()
engine = create_engine('postgresql://nags_dbuser:c0ns0le@localhost:5432/nags')
Session=sessionmaker(bind=engine)

nag_table = Table(
        'nags', meta,
        Column('name', String(length=None),  primary_key=True, nullable=False),
        Column('created_date', DateTime(timezone=False)),
        )

run_table = Table(
        'runs', meta,
        Column('id', Integer, primary_key=True),
        Column('location', String, nullable=False),
        Column('nag', String, nullable=False),
        Column('start_time', DateTime, nullable=False),
        Column('created_date', DateTime(timezone=False)),
        )

class Nag(object):

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()

    def __repr__(self):
        return "<Nag('%s')>" % (self.name)

class Run(object):

    def __init__(self, location, nag, time):
        self.location = location
        self.nag = nag
        self.start_time= time
        self.created_date = datetime.now()

    def __repr__(self):
        return"<Run('%s'at'%s'at'%s')>" % (self.nag, self.location, str(self.time))

mapper(Nag, nag_table)
mapper(Run, run_table)

