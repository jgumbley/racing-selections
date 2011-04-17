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

class Nag(object):

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()

    def __repr__(self):
        return "<Nag('%s')>" % (self.name)

mapper(Nag, nags)

def create_tables():
    Session=sessionmaker(bind=engine)
    session=Session()
    nag1 = Nag("RED RUM")
    session.add(nag1)
    session.commit()

if __name__=='__main__':
    print "yo bliar"
    create_tables()
