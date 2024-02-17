import models, schemas,oauth2, db
from fastapi import Depends,HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["reminder"],
    prefix="/reminder"
)


@router.post("/add",status_code=201)
def add_medicine_reminder(reminderIn:schemas.MedicineReminderIn, db:Session=Depends(db.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    reminder = models.MedicineReminder(**reminderIn.model_dump(), user_id=current_user.id)

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return {"detail":"success"}

@router.get("/get",status_code=200,response_model=list[schemas.MedicineReminderOut])
def get_medicine_reminders(db:Session=Depends(db.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    reminders = db.query(models.MedicineReminder).filter(models.MedicineReminder.user_id == current_user.id).all()

    return reminders

@router.delete("/delete/{id}",status_code=202)
def delete_reminder(id:int, db:Session=Depends(db.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    reminder = db.query(models.MedicineReminder).filter(models.MedicineReminder.id == id).first()

    db.delete(reminder)
    db.commit()

    return {"detail":"deleted"}