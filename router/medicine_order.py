from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User,Pharmacy, MedicineOrder
from db import get_db
from schemas import MedicineOrderCreate, MedicineOrderOut
from oauth2 import get_current_user

router = APIRouter(
    tags=["medicine_order"],
    prefix="/medicine_order"
)
   
@router.post("/create")
def create_medicine_order(medicine_order:MedicineOrderCreate, db:Session = Depends(get_db)):
    medicine_order = MedicineOrder(**medicine_order)
    medicine_order.delivered = 0
    db.add(medicine_order)
    db.commit()
    db.refresh(medicine_order)
    return medicine_order

@router.put("update/{id}")
def update_medicine_order(id:int, db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):

    if current_user.role != "PHARMACY":
        raise HTTPException(status_code=401, detail="Not Authorized")
    medicine_order = db.query(MedicineOrder).filter(MedicineOrder.id == id).first()
    if not medicine_order:
        raise HTTPException(status_code=404, detail="Not Found")
    
    medicine_order.pharmacy_id = current_user.id

    pharmacy = db.query(Pharmacy).join(User).filter(User.id == current_user.id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Invaild Pharmacy")
    
    pharmacy.balance += medicine_order.price
    db.add(medicine_order)
    db.add(pharmacy)
    db.commit()

    return HTTPException(status_code=200, detail="Updated medicine order")

@router.get("/available/all",status_code=200)
def get_available_medicine_orders(db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if current_user.role == "PHARMACY":
        medicine_order = db.query(MedicineOrder).filter(MedicineOrder.pharmacy_id == None).filter(MedicineOrder.delivered==0).all()
        available_medicine_order = []
        for order in medicine_order:
            orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=order.user.name, description = order.description, place = order.place, price = order.price,phone = order.user.phone)
            available_medicine_order.append(orderschema)

        return available_medicine_order
    else:
        raise HTTPException(status_code=401, detail="Not Authorized")
    
    
@router.get("/undelivered/all",status_code=200)
def get_pending_medicine_orders(db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if current_user.role == "PHARMACY":
        medicine_order = db.query(MedicineOrder).filter(MedicineOrder.pharmacy_id == current_user.id).filter(MedicineOrder.delivered==0).all()

        available_medicine_order = []
        for order in medicine_order:
            orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=order.user.name, description = order.description, place = order.place, price = order.price,phone = order.user.phone)
            available_medicine_order.append(orderschema)
        
        return available_medicine_order

    elif current_user.role == "USER":
        medicine_order = db.query(MedicineOrder).filter(MedicineOrder.user_id == current_user.id).filter(MedicineOrder.delivered==0).all()
        available_medicine_order = []
        for order in medicine_order:
            orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=order.pharmacy.name, description = order.description, place = order.place, price = order.price,phone = order.pharmacy.user.phone)
            available_medicine_order.append(orderschema)

        return available_medicine_order

    else:
        raise HTTPException(status_code=401, detail="Not Authorized")
        
@router.put("/update/delivery/{id}",status_code=200)
def update_delivery(id:int, db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    if current_user.role == "PHARMACY":
        medicine_order = db.query(MedicineOrder).filter(MedicineOrder.id == id).filter(MedicineOrder.pharmacy_id == current_user.id).first()
        if not medicine_order:
            raise HTTPException(status_code=404, detail="Not Found")
        
        medicine_order.delivered = 1
        db.add(medicine_order)
        db.commit()
        return HTTPException(status_code=200, detail="Updated medicine order")
    else:
        raise HTTPException(status_code=401, detail="Not Authorized")

