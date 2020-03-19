from datetime import date

from instanses import User, Purchase, content, users_relatives
from base import Base, Session, engine


Base.metadata.create_all(engine)
session = Session()

