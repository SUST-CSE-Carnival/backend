import models, schemas, utils, oauth2, db
from fastapi import Depends,HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["authentication"]
)

@router.post("/signin", response_model=schemas.Token)
def signin(userCredentials:schemas.UserSignin, db:Session = Depends(db.get_db)):
     
    user = db.query(models.User).filter(models.User.email == userCredentials.email ).first()
    if not user:
        raise HTTPException(status_code= 404, 
                            detail=f"User with email not found")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=404, detail="error")
    
    

    accessToken = oauth2.createAccessToken(data = {"id":user.id, 
                                                    "email":user.email,
                                                    "role":user.role,
                                                    "name":user.name,
                                                    "phone":user.phone})
    tokenData = schemas.Token(id=user.id ,accessToken=accessToken,token_type="Bearer", email=user.email, name=user.name, url=user.url,phone = user.phone,role=user.role)

    return tokenData



@router.post("/signup",
             status_code= 201,
             response_model= schemas.UserOut)
def signup(user:schemas.UserSignup, db:Session = Depends(db.get_db)):
    userT = db.query(models.User).filter(models.User.email == user.email).first()
    if userT:
        raise HTTPException(status_code=404, detail="User already exists")
    user.password = utils.hash(user.password)
    user = models.User(**user.model_dump())
    user.role ="USER"
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/pharmacy/signup")
def pharmacySignup(pharmacy:schemas.PharmacySignup, db:Session = Depends(db.get_db)):
    userT = db.query(models.User).filter(models.User.email == user.email).first()
    if userT:
        raise HTTPException(status_code=404, detail="User already exists")
    user = pharmacy.user
    user.password = utils.hash(user.password)
    user = models.User(**user.model_dump())
    user.role ="PHARMACY"
    db.add(user)
    db.commit()
    db.refresh(user)
    pharmacy = models.Pharmacy(pharmacy_name=pharmacy.pharmacy_name, bio=pharmacy.bio, place=pharmacy.place, user=user)
    pharmacy.balance = 0
    db.add(pharmacy)
    db.commit()
    db.refresh(pharmacy)
    return pharmacy

@router.get("/profile",response_model=schemas.UserSchema)
def profile(db:Session = Depends(db.get_db),current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return current_user
    
    
