from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

# inherit your models from this class to create proper database table and columns
Base = declarative_base()


# creating the db model for user
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)  # Sequence = auto increase by 1
    telegram_id = Column(Integer, unique=True)
    username = Column(String(15))
    surname = Column(String(15))
    team = Column(String(15))
