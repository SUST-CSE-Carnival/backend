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

# Create an instance of the FastAPI application
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a context manager for the application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create an AsyncIOScheduler instance
    scheduler = AsyncIOScheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    # Create a job to send medicine reminders every 1 minute
    trigger = IntervalTrigger(minutes=1)
    scheduler.add_job(sendMedincineReminders, trigger=trigger)

    # Yield control to the application
    yield

    # Shutdown the scheduler when the application is shutting down
    scheduler.shutdown()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Define the root route
@app.get("/")
def read_root():
    """
    Root endpoint of the SUST Project Backend.

    Returns:
        dict: A dictionary containing the introduction message.
    """
    return {"Intro": "SUST Project Backend"}

# Include the routers for different endpoints
app.include_router(auth.router)
app.include_router(medicine.router)
app.include_router(medicine_order.router)
app.include_router(medicine_reminder.router)
app.include_router(review.router)
