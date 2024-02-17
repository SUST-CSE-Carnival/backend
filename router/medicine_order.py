from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User,Pharmacy, MedicineOrder,Medicine
from db import get_db
from schemas import MedicineOrderCreate, MedicineOrderOut, MedicineOrderInOCR, MedicineOrderOutOCR
from oauth2 import get_current_user

router = APIRouter(
    tags=["medicine_order"],
    prefix="/medicine_order"
)

@router.post("/ocr/create")
def create_medicine_order_ocr(list:MedicineOrderInOCR, db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    
    if current_user.role != "USER":
        raise HTTPException(status_code=401, detail="Not Authorized")

    cost = 0
    return_list = MedicineOrderOutOCR(price=0,medicines=[])
    for medicine in list.medicines:
       medicine_db = db.query(Medicine).filter(Medicine.medicine_name.ilike(f"%{medicine.name}%")).first()
       if medicine_db:
            cost += medicine_db.price*medicine.quantity
            return_list.medicines.append(medicine)
    
    return_list.price +=cost

    return return_list

   
@router.post("/create")
def create_medicine_order(order:MedicineOrderCreate, db:Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    medicine_order = MedicineOrder(description=order.description, place=order.place, price=order.price, user = current_user)
    medicine_order.delivered = 0
    medicine_order.reviewChecked = 0
    db.add(medicine_order)
    db.commit()
    db.refresh(medicine_order)
    return HTTPException(status_code=201, detail="Success")  

@router.put("/update/{id}")
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
            orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=order.user.name,email=order.user.email, description = order.description, place = order.place, price = order.price,phone = order.user.phone)
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
            orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=order.user.name,email=order.user.email, description = order.description, place = order.place, price = order.price,phone = order.user.phone)
            available_medicine_order.append(orderschema)
        
        return available_medicine_order

    elif current_user.role == "USER":
        medicine_order = db.query(MedicineOrder).filter(MedicineOrder.user_id == current_user.id).filter(MedicineOrder.delivered==0).all()
        available_medicine_order = []
        for order in medicine_order:
            if order.pharmacy is None:
                orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name="null",email ="null", description = order.description, place = order.place, price = order.price,phone = "null")
            else:
                pharmacy_shop = db.query(Pharmacy).join(User).filter(User.id == order.pharmacy.id).first()
                orderschema = MedicineOrderOut(id = order.id, user_id = order.user_id, name=pharmacy_shop.pharmacy_name,email=order.pharmacy.email, description = order.description, place = order.place, price = order.price,phone = order.pharmacy.phone)
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

