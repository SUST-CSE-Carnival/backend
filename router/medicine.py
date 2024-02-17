from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Medicine
from db import get_db
from schemas import MedicineOut

router = APIRouter(
    tags=["medicine"],
    prefix="/medicine"
)

@router.get("/all", response_model=list[MedicineOut],status_code=200)
def get_all_medicines(db:Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    return medicines       



   