from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from utils import sendMedincineReminders
from db import engine 
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from router import auth,medicine,medicine_order,medicine_reminder,review



scheduler = AsyncIOScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = IntervalTrigger(seconds=30)  
    scheduler.add_job(sendMedincineReminders, trigger=trigger)
    yield   
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Intro": "SUST Project Backend"}

# Include the routers for different endpoints
app.include_router(auth.router)
app.include_router(medicine.router)
app.include_router(medicine_order.router)
app.include_router(medicine_reminder.router)
app.include_router(review.router)
