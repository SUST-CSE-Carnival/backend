from pydantic import BaseModel,EmailStr


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
    user_id:int
    pharmacy_id:int
    description:str
    place:str
    price:int

    class Config:
        orm_mode = True


class MedicineOrderOut(BaseModel):
    id:int
    user_id:int
    name:str
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

