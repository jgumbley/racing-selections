from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from datetime import datetime

engine = create_engine('postgresql://nags_dbuser:c0ns0le@localhost:5432/nags')

Base = declarative_base()

Session=sessionmaker(bind=engine)

class Nag(Base):
    __tablename__ = 'nags'

    name =          Column(String, primary_key=True)
    created_date =  Column(DateTime)

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.now()

    def __repr__(self):
        return "<Nag('%s')>" % (self.name)

def create_tables():
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    nag1 = Nag("RED RUM")
    session.add(nag1)
    session.commit()

if __name__=='__main__':
    print "yo bliar"
    create_tables()
