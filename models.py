from db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

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


class Pharmacy(Base):
    __tablename__ = 'pharmacies'
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    bio = Column(String, nullable=False)
    pharmacy_name = Column(String)
    place = Column(String)
    balance = Column(Integer)

class Medicine(Base):
    __tablename__ = 'medicines'
    id = Column(Integer, primary_key=True,index=True)
    manufacturer_name = Column(String, nullable=False)
    medicine_name = Column(String, nullable=False)
    generic_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    
class MedicineOrder(Base):
    __tablename__ = 'medicine_orders'
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[user_id])
    pharmacy_id = Column(Integer, ForeignKey('users.id'))
    pharmacy = relationship("User",foreign_keys=[pharmacy_id])
    description = Column(Text, nullable=False)
    place = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    delivered = Column(Integer, nullable=False)
    reviewChecked = Column(Integer, nullable=False)


class MedicineReminder(Base):
    __tablename__ = 'medicine_reminders'
    id = Column(Integer, primary_key=True,index=True)
    description = Column(String, nullable=False)
    time = Column(String, nullable=False)
    days=Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True,index=True)
    starCount = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"))   
    reviewer =relationship("User", foreign_keys=[reviewer_id])
    subject_id = Column(Integer, ForeignKey("users.id"))
    subject =relationship("User", foreign_keys=[subject_id])


    
