
from typing import List
import oauth2, db
from fastapi import Depends,HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import User, Review, MedicineOrder, Pharmacy
from schemas import ReviewIn, ReviewOut, ReviewPending

router = APIRouter(
    tags=["review"],
    prefix="/review",
)


@router.post("/add",status_code=201)
def addReview(review:str,star:int, reviewin: ReviewIn, db:Session=Depends(db.get_db), current_user: User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER":
        raise HTTPException(status_code=401, detail="Not Authorized")

    review = Review(review=review,starCount=star,reviewer_id=current_user.id,subject_id=reviewin.subjectId)

    medicine_order = db.query(MedicineOrder).filter(MedicineOrder.id == reviewin.orderId).first()

    medicine_order.reviewchecked = 1
    db.add(medicine_order)
    db.commit()
    db.add(review)
    db.commit()

    return {"details":"success"}


@router.get("/pending")
def getPendingReview(db:Session=Depends(db.get_db), current_user: User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER":
        raise HTTPException(status_code=401, detail="Not Authorized")

    medicine_orders = db.query(MedicineOrder) .filter(MedicineOrder.user_id == current_user.id).filter(MedicineOrder.reviewChecked == 0).all()

    reviewsout = []
    for i in medicine_orders:
        if(i.pharmacy is None):
            continue
        pharmacyshop =db.query(Pharmacy).join(User).filter(User.id == i.pharmacy.id).first()
        reviewout= ReviewPending(orderId=i.id,subjectId=i.pharmacy.id,pharmacy_name=pharmacyshop.pharmacy_name)
        reviewsout.append(reviewout)
    
    return reviewsout

@router.get("/{id}")
def getReview(id:int, db:Session=Depends(db.get_db), current_user: User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER" and current_user.role!="PHARMACY":
        raise HTTPException(status_code=404, detail="Not Authorized")

    reviews = db.query(Review).filter(Review.subject_id == id).all()
    reviewsout = []
    for i  in reviews:
        reviewout= ReviewOut(id=i.id,review=i.review,starCount=i.starCount,reviewerId=i.reviewer_id,subjectId=i.subject_id, reviewerName=i.reviewer.name)
        reviewsout.append(reviewout)
    
    return reviewsout



