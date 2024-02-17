from db import Base
from sqlalchemy import Column, Integer, String, Text

#User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    name = Column(String, nullable= False)
    url = Column(Text, nullable=True)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False)



