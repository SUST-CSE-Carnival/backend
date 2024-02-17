from pydantic import BaseModel,EmailStr
from typing import List
class UserSchema(BaseModel):
    id:int
    email:EmailStr
    name:str
    url:str
    role:str
    phone:str

    class Config:
        orm_mode = True



class Token(BaseModel):
    id :int
    accessToken:str
    token_type: str
    email:EmailStr
    role:str
    phone:str
    name:str
    url:str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id:int

class UserSignup(BaseModel):
    email:EmailStr
    password:str
    name:str
    url:str
    phone:str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    url:str
    role:str
    phone:str

    class Config:
        orm_mode = True


class UserSignin(BaseModel):
    email:EmailStr
    password:str


class PharmacySignup(BaseModel):
   user : UserSignup
   pharmacy_name:str
   bio:str
   place:str


class MedicineOut(BaseModel):
    id:int
    manufacturer_name:str
    medicine_name:str
    generic_name:str
    price:int

    class Config:
        orm_mode = True


class MedicineOrderCreate(BaseModel):
    description:str
    place:str
    price:int

    class Config:
        orm_mode = True


class MedicineOCR(BaseModel):
    name:str
    quantity:int

class MedicineOrderInOCR(BaseModel):
    medicines:List[MedicineOCR]

class MedicineOrderOutOCR(BaseModel):
    medicines:List[MedicineOCR]
    price :int


class MedicineOrderOut(BaseModel):
    id:int
    user_id:int
    name:str
    email:str
    description:str
    place:str
    price:int
    phone:str

    class Config:
        orm_mode = True

class MedicineReminderIn(BaseModel):
    description:str
    time:str
    days:str
    api_key:str



class MedicineReminderOut(BaseModel):
    id:int
    description:str
    time:str
    days:str

    class Config():
        orm_mode = True


class ReviewIn(BaseModel):
    subjectId:int
    orderId:int

class ReviewOut(BaseModel):
    id:int
    subjectId:int
    reviewerId:int
    reviewerName:str
    review:str
    starCount:int

    class Config:
        orm_mode = True

class ReviewPending(BaseModel):
    orderId:int
    subjectId:int
    pharmacy_name:str

    class Config():
        orm_mode = True

