from datetime import date, timedelta,datetime
from enum import Enum
from passlib.context import CryptContext
pwdContext = CryptContext(schemes=["bcrypt"], deprecated ="auto")
from fastapi import Depends


def hash(password:str):
    return pwdContext.hash(password)

def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)