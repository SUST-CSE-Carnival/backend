from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from db import engine
from router import auth,medicine,medicine_order,medicine_reminder

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Intro": "SUST Project Backend"}


app.include_router(auth.router)
app.include_router(medicine.router)
app.include_router(medicine_order.router)
app.include_router(medicine_reminder.router)
