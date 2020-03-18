from datetime import date

from instanses import User, Purchase, content, family_mode
from base import Base, Session, engine


Base.metadata.create_all(engine)
session = Session()

