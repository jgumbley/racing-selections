
## File autogenerated by genmodel.py

from sqlalchemy import *
meta = MetaData()


nags = Table('nags', meta,
  Column('name', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  primary_key=True, nullable=False),
  Column('created_date', DateTime(timezone=False)),
)

mapper(User, users_table)
