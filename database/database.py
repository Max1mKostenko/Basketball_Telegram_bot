from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os


# saving of db file
basedir = os.path.abspath(os.path.dirname(__file__))

# getting to database file
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../user.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# initializing and connecting to database
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# database session to write/upd/delete data
Session = sessionmaker(bind=engine)
