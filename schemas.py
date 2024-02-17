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

class UserSignup(BaseModel):
    email:EmailStr
    password:str
    name:str
    url:str
    phone:str

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    url:str
    role:str
    phone:str

class UserSignin(BaseModel):
    email:EmailStr
    password:str