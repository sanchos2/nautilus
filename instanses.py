from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from base import Base

#**************************************************
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String)
    pas = Column(String)
    nick_name = Column(String)
    telegram_id = Column(String)
    email = Column(String)
    fns_login = Column(String)
    fns_pas = Column(String)


class Purchase(Base):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    fn_number = Column(String)
    fpd_number = Column(String)
    check_type = Column(String)
    date = Column(Date)
    sums = Column(Integer)


content = Table('content', Base.metadata,
    Column('check_id', Integer, ForeignKey('purchase.id')),
    Column('product', String),
    Column('price', Integer),
    Column('quantity', Integer),
    Column('sum', Integer),
    Column('category', String),
    Column('subcategory', Integer)
)

users_relatives = Table('users_relatives', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('relative', Integer, ForeignKey('users.id')),
)