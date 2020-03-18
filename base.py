from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

path_to_file = os.path.dirname(__file__)
bd_name = 'project.bd'
path_for_engine = f'sqlite:///{path_to_file}//{bd_name}'
print(path_to_file)

engine = create_engine(path_for_engine)
Session = sessionmaker(bind= engine)

Base = declarative_base()
